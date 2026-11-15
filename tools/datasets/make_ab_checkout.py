#!/usr/bin/env python3
"""Generator for data/ab_checkout.csv  (SPOILERS inside).

A fictional Indian shopping app tests a redesigned one-page checkout (treatment) against the old three-step checkout
(control) for 21 days from 2025-02-03. One row per user assignment. Planted problems: sample-ratio mismatch (a redirect bug
drops low-end Android users from treatment), a novelty effect, heavy-tailed revenue, users seen in both arms, mixed time zones.
Deterministic: fixed seed, numpy + pandas only. Run: python3 tools/datasets/make_ab_checkout.py [--out DIR]
"""
import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20250203
START = pd.Timestamp("2025-02-03")
N_USERS = 15000
DAYS = 21
DEVICES = ["Android mid/high", "Android low-end", "iOS", "Web"]
DEVICE_P = [0.46, 0.20, 0.14, 0.20]
BASE_P = {"Android mid/high": 0.12, "Android low-end": 0.05, "iOS": 0.16, "Web": 0.10}
P_DROP_LOWEND_TREATMENT = 0.55
EFFECT_NEW = 0.80            # log-odds lift for new users on day 0, decays as exp(-day/4)
EFFECT_RET = 0.25
DECAY_DAYS = 4.0
P_ERR = {"control": 0.045, "treatment": 0.052}
BULK_SHARE = 0.0035          # share of converters who place a bulk (B2B style) order


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    n = N_USERS
    uid = 20000001 + np.cumsum(rng.integers(1, 4, n))
    user_id = np.array([f"U{u}" for u in uid], dtype=object)
    rng.shuffle(user_id)
    day = np.minimum(rng.integers(0, DAYS, n) + (rng.random(n) < 0.12) * 0, DAYS - 1)
    day = np.where(rng.random(n) < 0.5, rng.integers(0, 7, n), day)            # a bit more traffic in week 1
    hour = np.clip(np.round(rng.normal(20, 3.5, n)), 0, 23).astype(int)
    minute = rng.integers(0, 60, n); sec = rng.integers(0, 60, n)
    ts = START + pd.to_timedelta(day, unit="D") + pd.to_timedelta(hour * 3600 + minute * 60 + sec, unit="s")
    device = rng.choice(DEVICES, size=n, p=DEVICE_P)
    new_user = rng.random(n) < 0.45
    tier = rng.choice(["Tier 1", "Tier 2", "Tier 3"], size=n, p=[0.38, 0.34, 0.28])
    source = rng.choice(["organic", "paid_social", "paid_search", "email", "direct"], size=n, p=[0.35, 0.25, 0.20, 0.10, 0.10])
    pre_orders = np.where(new_user, 0, np.minimum(rng.poisson(1.4, n), 8))
    pre_spend = np.where(pre_orders > 0, np.round(pre_orders * np.exp(rng.normal(np.log(900), 0.6, n)), 0), 0.0)
    variant = np.where(rng.random(n) < 0.5, "treatment", "control")

    p0 = np.array([BASE_P[d] for d in device])
    logit = np.log(p0 / (1 - p0)) + 0.35 * (~new_user) + 0.10 * np.minimum(pre_orders, 4) - 0.08 * (tier == "Tier 3")
    logit = logit + rng.normal(0, 0.35, n)                               # unobserved user intent
    eff = np.where(new_user, EFFECT_NEW, EFFECT_RET) * np.exp(-day / DECAY_DAYS)
    p_conv = sigmoid(logit + np.where(variant == "treatment", eff, 0.0))
    p_conv_ctrl = sigmoid(logit)
    converted = rng.random(n) < p_conv
    order_value = np.round(np.exp(rng.normal(np.log(1100), 0.8, n)), 0)
    bulk = converted & (rng.random(n) < BULK_SHARE)
    order_value = np.where(bulk, np.round(rng.uniform(150000, 900000, n), -3), order_value)
    revenue = np.where(converted, order_value, 0.0)
    pay_err = rng.random(n) < np.where(variant == "treatment", P_ERR["treatment"], P_ERR["control"])

    # sample-ratio mismatch: the redirect bug silently drops low-end Android users who were assigned to treatment
    dropped = (variant == "treatment") & (device == "Android low-end") & (rng.random(n) < P_DROP_LOWEND_TREATMENT)
    keep = ~dropped

    df = pd.DataFrame({"user_id": user_id, "assign_ts": ts, "variant": variant, "device_class": device,
                       "new_user": new_user.astype(int), "city_tier": tier, "traffic_source": source,
                       "pre_orders_30d": pre_orders, "pre_spend_30d": pre_spend, "converted": converted.astype(int),
                       "revenue_inr": revenue, "payment_error": pay_err.astype(int)})
    df["day_index"] = day
    df["p_conv_ctrl"] = p_conv_ctrl
    df["p_conv_actual"] = p_conv
    df["bulk"] = bulk
    full = df.copy()
    df = df[keep].reset_index(drop=True)

    # users seen in BOTH arms (cookie reset): copy 1.2% of rows into the other arm, outcome re-drawn
    k = int(round(0.012 * len(df)))
    pick = rng.choice(len(df), size=k, replace=False)
    twin = df.iloc[pick].copy()
    twin["variant"] = np.where(twin["variant"] == "control", "treatment", "control")
    tw_eff = np.where(twin["new_user"] == 1, EFFECT_NEW, EFFECT_RET) * np.exp(-twin["day_index"].to_numpy() / DECAY_DAYS)
    tw_p = np.where(twin["variant"] == "treatment", sigmoid(np.log(twin["p_conv_ctrl"] / (1 - twin["p_conv_ctrl"])) + tw_eff), twin["p_conv_ctrl"])
    twin["converted"] = (rng.random(len(twin)) < tw_p).astype(int)
    twin["revenue_inr"] = np.where(twin["converted"] == 1, np.round(np.exp(rng.normal(np.log(1100), 0.8, len(twin))), 0), 0.0)
    twin["assign_ts"] = twin["assign_ts"] + pd.to_timedelta(rng.integers(1, 40, len(twin)), unit="m")
    df = pd.concat([df, twin], ignore_index=True)
    df = df.sort_values("assign_ts", kind="stable").reset_index(drop=True)
    truth = {"n_assigned_users": n, "n_dropped_treatment_lowend": int(dropped.sum()), "n_twin_users": k,
             "full": full, "effect_new": EFFECT_NEW, "effect_ret": EFFECT_RET, "decay_days": DECAY_DAYS,
             "true_ctrl_conv_rate": float(full["p_conv_ctrl"].mean())}

    # ---------- messiness
    n2 = len(df)
    iso = [f"{t.year:04d}-{t.month:02d}-{t.day:02d}T{t.hour:02d}:{t.minute:02d}:{t.second:02d}+05:30" for t in df["assign_ts"]]
    utc_rows = rng.random(n2) < 0.03                               # logging bug: some rows written in UTC with a Z suffix
    out_ts = []
    for s, t, u in zip(iso, df["assign_ts"], utc_rows):
        if u:
            tt = t - pd.Timedelta(hours=5, minutes=30)
            out_ts.append(f"{tt.year:04d}-{tt.month:02d}-{tt.day:02d}T{tt.hour:02d}:{tt.minute:02d}:{tt.second:02d}Z")
        else:
            out_ts.append(s)
    out = df[["user_id", "variant", "device_class", "new_user", "city_tier", "traffic_source", "pre_orders_30d", "pre_spend_30d", "converted", "revenue_inr", "payment_error"]].copy()
    out.insert(1, "assign_ts", out_ts)
    out["city_tier"] = np.where(rng.random(n2) < 0.03, "", out["city_tier"])
    src = out["traffic_source"].to_numpy(dtype=object)
    src[(df["device_class"].to_numpy() == "Web") & (rng.random(n2) < 0.25)] = "unknown"
    out["traffic_source"] = src
    dc = out["device_class"].to_numpy(dtype=object); dc[rng.random(n2) < 0.01] = ""
    out["device_class"] = dc
    truth["day_index"] = df["day_index"].to_numpy(); truth["utc_rows"] = utc_rows
    return out, truth


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    out_dir = Path(args.out) if args.out else root / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    df, truth = generate()
    path = out_dir / "ab_checkout.csv"
    o = df.copy()
    o["pre_spend_30d"] = o["pre_spend_30d"].map(lambda v: f"{v:.0f}")
    o["revenue_inr"] = o["revenue_inr"].map(lambda v: f"{v:.0f}")
    o.to_csv(path, index=False, lineterminator="\n")
    raw = path.read_bytes()
    print(f"ab_checkout.csv: {len(df)} rows, {df.shape[1]} columns, {len(raw):,} bytes, sha256 {hashlib.sha256(raw).hexdigest()[:12]}")
    print(f"  treatment share {(df['variant'] == 'treatment').mean():.4f}; conversion control {df.loc[df.variant == 'control', 'converted'].mean():.4f} treatment {df.loc[df.variant == 'treatment', 'converted'].mean():.4f}")


if __name__ == "__main__":
    main()
