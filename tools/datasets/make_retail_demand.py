#!/usr/bin/env python3
"""Generator for data/retail_demand.csv  (SPOILERS inside).

A fictional Indian supermarket chain: daily store x SKU sales, 2023-01-01 to 2024-12-31. Demand is built from weekday, season,
moving festivals, promotions and trend; an inventory rule then CENSORS sales when stock runs out (sales = min(demand, stock)).
Deterministic: fixed seed, numpy + pandas only. Run: python3 tools/datasets/make_retail_demand.py [--out DIR]
"""
import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20231112
DAYS = pd.date_range("2023-01-01", "2024-12-31")
STORES = [("S1", "Mumbai", 1.30), ("S2", "Bengaluru", 1.10), ("S3", "Delhi", 1.20), ("S4", "Kolkata", 0.90), ("S5", "Chennai", 0.95)]
SKUS = [("SKU01", "Packaged Milk 1L", 55.0, 66, "stable"), ("SKU02", "Cold Drink 2L", 30.0, 95, "summer"),
        ("SKU03", "Dry Fruit Gift Box", 4.0, 899, "diwali"), ("SKU04", "Umbrella", 1.2, 449, "monsoon"),
        ("SKU05", "Instant Noodles 4-pack", 22.0, 56, "promo"), ("SKU06", "Olive Oil 500ml", 1.5, 549, "slow")]
DOW_MULT = np.array([0.92, 0.90, 0.93, 0.96, 1.05, 1.22, 1.18])           # Monday first
ELASTICITY = -2.5
FEST = {  # name -> dates (verified calendar dates)
    "Pongal": ["2023-01-15", "2024-01-15"], "Holi": ["2023-03-08", "2024-03-25"], "Eid al-Fitr": ["2023-04-22", "2024-04-11"],
    "Raksha Bandhan": ["2023-08-30", "2024-08-19"], "Ganesh Chaturthi": ["2023-09-19", "2024-09-07"],
    "Dussehra": ["2023-10-24", "2024-10-12"], "Diwali": ["2023-11-12", "2024-11-01"], "Christmas": ["2023-12-25", "2024-12-25"],
    "Durga Puja Ashtami": ["2023-10-22", "2024-10-11"]}
# (kind or '*') -> {festival: (days_before, peak_multiplier)}
FEST_EFFECT = {"diwali": {"Diwali": (12, 3.4), "Raksha Bandhan": (4, 1.8), "Christmas": (6, 1.6), "Dussehra": (3, 1.3)},
               "summer": {"Holi": (2, 1.5), "Eid al-Fitr": (1, 1.2)},
               "slow": {"Diwali": (7, 1.5)}, "stable": {"Diwali": (1, 1.12), "Eid al-Fitr": (1, 1.12), "Christmas": (1, 1.12)}}
KOLKATA_PUJA = {"diwali": (5, 1.5), "summer": (3, 1.2)}
OUTAGE = ("2023-06-14", "2023-06-16")
S3_GAP = ("2024-02-05", "2024-02-18")
S2_CLOSED = ("2023-09-04", "2023-09-17")


def seasonality(kind, doy):
    if kind == "summer":
        return 1 + 0.55 * np.sin(2 * np.pi * (doy - 45) / 365)
    if kind == "monsoon":
        return 0.25 + 3.0 * np.exp(-0.5 * ((doy - 190) / 30.0) ** 2)
    if kind == "diwali":
        return 0.9 + 0.1 * np.cos(2 * np.pi * (doy - 15) / 365)
    return 1 + 0.04 * np.sin(2 * np.pi * doy / 365)


def festival_mult(kind, store_id):
    m = np.ones(len(DAYS))
    eff = dict(FEST_EFFECT.get(kind, {}))
    for fest, (pre, peak) in eff.items():
        for ds in FEST[fest]:
            i = int((pd.Timestamp(ds) - DAYS[0]).days)
            for k in range(pre + 1):
                if 0 <= i - k < len(m):
                    m[i - k] = max(m[i - k], 1 + (peak - 1) * (1 - k / (pre + 1)))
    if store_id == "S4" and kind in KOLKATA_PUJA:
        pre, peak = KOLKATA_PUJA[kind]
        for ds in FEST["Durga Puja Ashtami"]:
            i = int((pd.Timestamp(ds) - DAYS[0]).days)
            for k in range(pre + 1):
                if 0 <= i - k < len(m):
                    m[i - k] = max(m[i - k], 1 + (peak - 1) * (1 - k / (pre + 1)))
    return m


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    T = len(DAYS)
    doy = DAYS.dayofyear.to_numpy(); dow = DAYS.dayofweek.to_numpy()
    fest_name = np.array([""] * T, dtype=object)
    for f, ds in FEST.items():
        for d in ds:
            fest_name[int((pd.Timestamp(d) - DAYS[0]).days)] = f
    trend = 1 + 0.12 * np.arange(T) / T
    rows = []
    truth = {"demand_total": 0.0, "lost_total": 0.0, "censored_days": 0, "series_days": 0}
    closed_idx = (DAYS >= pd.Timestamp(S2_CLOSED[0])) & (DAYS <= pd.Timestamp(S2_CLOSED[1]))
    for sid, city, scale in STORES:
        temp_base = {"Mumbai": 29, "Bengaluru": 26, "Delhi": 26, "Kolkata": 28, "Chennai": 30}[city]
        amp = 9.0 if city == "Delhi" else 4.0
        temp = np.round(temp_base + amp * np.sin(2 * np.pi * (doy - 110) / 365) + rng.normal(0, 1.5, T), 1)
        for skid, name, base, price, kind in SKUS:
            mu = base * scale * DOW_MULT[dow] * seasonality(kind, doy) * festival_mult(kind, sid) * trend
            if kind == "summer":
                mu = mu * (1 + 0.03 * np.clip(temp - 30, -8, 10))
            promo = np.zeros(T, dtype=int); disc = np.zeros(T)
            if kind in ("summer", "promo", "stable"):
                t = 0
                while t < T:
                    boost = 2.0 if (kind == "summer" and 4 <= DAYS[t].month <= 6) else 1.0
                    if rng.random() < 0.022 * boost * (1.4 if kind == "promo" else 1.0):
                        L = int(rng.integers(3, 8)); dsc = float(rng.choice([0.10, 0.15, 0.20, 0.25]))
                        promo[t:t + L] = 1; disc[t:t + L] = dsc
                        t += L + 4
                    else:
                        t += 1
            lift = np.where(promo == 1, (1 - disc) ** ELASTICITY, 1.0)
            post = np.zeros(T)
            for i in np.flatnonzero((promo[:-1] == 1) & (promo[1:] == 0)):
                post[i + 1:i + 6] = 1
            mu = mu * lift * np.where(post == 1, 0.85, 1.0)
            lam = mu * rng.gamma(12.0, 1 / 12.0, T)
            demand = rng.poisson(lam)
            if sid == "S2":
                demand = np.where(closed_idx, 0, demand)
            # inventory: base-stock rule that ignores festivals; 2-day lead time
            base_mu = base * scale
            R, Tgt = int(np.ceil(base_mu * 2.2)) + 1, int(np.ceil(base_mu * 5.0)) + 2
            stock = Tgt; pipe = [0, 0]
            units = np.zeros(T, dtype=int); close = np.zeros(T, dtype=int)
            for t in range(T):
                stock += pipe.pop(0)
                s = min(int(demand[t]), stock)
                stock -= s; units[t] = s; close[t] = stock
                position = stock + sum(pipe)
                pipe.append(Tgt - position if position <= R else 0)
            cens = demand > units
            open_ = (~closed_idx if sid == "S2" else np.ones(T, dtype=bool))
            truth["demand_total"] += float(demand[open_].sum()); truth["lost_total"] += float((demand - units)[open_].sum())
            truth["censored_days"] += int(cens[open_].sum()); truth["series_days"] += int(open_.sum())
            truth.setdefault("series", {})[(sid, skid)] = {"demand": demand, "units": units}
            for t in range(T):
                rows.append((DAYS[t], sid, city, skid, name, int(units[t]), price, int(promo[t]), int(round(disc[t] * 100)), int(close[t]),
                             int(open_[t]) if sid == "S2" else 1, fest_name[t], float(temp[t])))
    df = pd.DataFrame(rows, columns=["date", "store_id", "store_city", "sku_id", "sku_name", "units_sold", "unit_price", "promo_flag",
                                     "discount_pct", "closing_stock", "store_open", "festival", "temp_c"])
    df["revenue_inr"] = np.round(df["units_sold"] * df["unit_price"] * (1 - df["discount_pct"] / 100.0), 2)
    # ---------- missing rows
    d = df["date"]
    drop = ((d >= pd.Timestamp(OUTAGE[0])) & (d <= pd.Timestamp(OUTAGE[1]))) | ((df["store_id"] == "S3") & (d >= pd.Timestamp(S3_GAP[0])) & (d <= pd.Timestamp(S3_GAP[1])))
    truth["rows_dropped"] = int(drop.sum())
    df = df[~drop].reset_index(drop=True)
    # ---------- price problems, negative units, spelling variants
    n = len(df)
    price = df["unit_price"].to_numpy(dtype=float).copy()
    pick = rng.choice(n, size=13, replace=False)
    price[pick[:8]] = 0.0; price[pick[8:]] = price[pick[8:]] * 100
    df["unit_price"] = price
    u = df["units_sold"].to_numpy().copy()
    pk = rng.choice(np.flatnonzero(u > 3), size=12, replace=False)
    u[pk] = -rng.integers(1, 4, 12)
    df["units_sold"] = u
    city_col = df["store_city"].to_numpy(dtype=object)
    for i in np.flatnonzero(rng.random(n) < 0.02):
        city_col[i] = {"Bengaluru": "Bangalore", "Kolkata": "Calcutta", "Mumbai": "Bombay"}.get(city_col[i], city_col[i].upper())
    df["store_city"] = city_col
    # ---------- dates: Kolkata POS exports dd/mm/yyyy
    ds = np.array([f"{t.year:04d}-{t.month:02d}-{t.day:02d}" for t in df["date"]], dtype=object)
    k = (df["store_id"] == "S4").to_numpy()
    ds[k] = [f"{t.day:02d}/{t.month:02d}/{t.year:04d}" for t in df["date"][k]]
    df["date"] = ds
    ex = rng.choice(n, size=30, replace=False)
    df = pd.concat([df, df.iloc[ex]], ignore_index=True)
    truth["n_dup_rows"] = 30
    truth["n_price_zero"] = 8; truth["n_price_x100"] = 5; truth["n_negative_units"] = 12
    return df, truth


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    out_dir = Path(args.out) if args.out else root / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    df, truth = generate()
    path = out_dir / "retail_demand.csv"
    o = df.copy()
    o["unit_price"] = o["unit_price"].map(lambda v: f"{v:.0f}")
    o["revenue_inr"] = o["revenue_inr"].map(lambda v: f"{v:.2f}")
    o["temp_c"] = o["temp_c"].map(lambda v: f"{v:.1f}")
    o.to_csv(path, index=False, lineterminator="\n")
    raw = path.read_bytes()
    print(f"retail_demand.csv: {len(df)} rows, {df.shape[1]} columns, {len(raw):,} bytes, sha256 {hashlib.sha256(raw).hexdigest()[:12]}")
    print(f"  censored store-SKU-days {truth['censored_days'] / truth['series_days']:.3f}; lost demand {truth['lost_total'] / truth['demand_total']:.3f} of true demand")


if __name__ == "__main__":
    main()
