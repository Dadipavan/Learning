#!/usr/bin/env python3
"""Generator for data/credit_loans.csv  (SPOILERS inside).

A fictional Indian digital lender: unsecured personal-loan applications, 2022-07 to 2024-06. The outcome `default_12m` is only
known for approved loans (reject-inference problem). Post-booking columns leak the outcome, repeat applicants break random
splits, thin-file applicants have no bureau score, and a stress period in 2024 hits gig workers.
Deterministic: fixed seed, numpy + pandas only. Run: python3 tools/datasets/make_credit_loans.py [--out DIR]
"""
import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20240630
N_BASE = 10000
D0, D1 = pd.Timestamp("2022-07-01"), pd.Timestamp("2024-06-30")
STRESS_FROM = pd.Timestamp("2024-01-01")
TARGET_DEFAULT_APPROVED = 0.085
EMP = ["Salaried", "Self-employed", "Gig/Platform", "Government"]
EMP_P = [0.55, 0.22, 0.15, 0.08]
INC_MED = {"Salaried": 42000, "Self-employed": 55000, "Gig/Platform": 24000, "Government": 52000}
EMP_EFF = {"Salaried": 0.0, "Self-employed": 0.25, "Gig/Platform": 0.40, "Government": -0.35}
PURPOSE = ["Medical", "Wedding", "Home renovation", "Debt consolidation", "Travel", "Education", "Business use"]


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def emi(p, rate_pct, n):
    r = rate_pct / 1200.0
    return p * r * (1 + r) ** n / ((1 + r) ** n - 1)


def calibrate(z, mask, target):
    lo, hi = -15.0, 5.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if sigmoid(z[mask] + mid).mean() > target:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def loan_level(rng, d, person):
    """Draw the loan-specific columns for rows described by `person` (dict of arrays)."""
    n = len(d["date"])
    inc = person["income"]
    d["loan_amount"] = np.clip(np.round(inc * rng.uniform(2, 9, n) / 5000) * 5000, 20000, 1500000)
    d["tenure"] = rng.choice([12, 18, 24, 36, 48, 60], size=n, p=[0.12, 0.10, 0.25, 0.30, 0.13, 0.10])
    score = person["score"]
    s_fill = np.where(np.isnan(score), 640.0, score)
    d["rate"] = np.round(np.clip(13 + 0.030 * (750 - s_fill) + np.where(person["emp"] == "Gig/Platform", 1.0, 0.0) + np.where(np.isnan(score), 3.0, 0.0), 11, 30), 1)
    new_emi = emi(d["loan_amount"], d["rate"], d["tenure"])
    d["foir"] = np.round((person["emi_existing"] + new_emi) / inc, 3)
    frac = (d["date"] - D0).days / (D1 - D0).days
    p_dig = 0.25 + 0.30 * np.asarray(frac)
    r = rng.random(n)
    d["channel"] = np.where(r < p_dig, "Digital", np.where(r < p_dig + (1 - p_dig) * 0.55, "DSA agent", "Branch"))
    d["purpose"] = rng.choice(PURPOSE, size=n, p=[0.16, 0.14, 0.18, 0.22, 0.08, 0.08, 0.14])
    return d


def decide(rng, d, person):
    score = person["score"]; thin = np.isnan(score); s_fill = np.where(thin, 640.0, score)
    foir, inc = d["foir"], person["income"]
    ok = ((s_fill >= 650) & ~thin | (thin & (foir < 0.40) & (person["emp"] != "Gig/Platform"))) & (foir < 0.55) & (inc >= 18000)
    n = len(foir)
    approved = np.where(ok, rng.random(n) >= 0.03, rng.random(n) < 0.04)
    z = (-0.011 * (s_fill - 700) + 2.2 * foir + 0.8 * person["util"] + 0.14 * person["enq"] + 0.45 * person["delinq"]
         - 0.30 * (np.log(inc) - np.log(40000)) + np.array([EMP_EFF[e] for e in person["emp"]]) + 0.15 * (person["tier"] == "Tier 3")
         + np.where(d["channel"] == "DSA agent", 0.30, np.where(d["channel"] == "Digital", 0.10, 0.0)) + np.where(thin, 0.5, 0.0)
         + np.where(person["age"] < 25, 0.25, 0.0) + person["u"]
         + np.where((d["date"] >= STRESS_FROM) & (person["emp"] == "Gig/Platform"), 0.7, 0.0))
    return approved, z


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    n = N_BASE
    dates = D0 + pd.to_timedelta(rng.integers(0, (D1 - D0).days + 1, n), unit="D")
    emp = rng.choice(EMP, size=n, p=EMP_P)
    age = np.clip(np.round(rng.normal(34, 8, n)), 21, 62).astype(int)
    tier = rng.choice(["Tier 1", "Tier 2", "Tier 3"], size=n, p=[0.35, 0.40, 0.25])
    income = np.round(np.array([INC_MED[e] for e in emp]) * np.exp(rng.normal(0, 0.5, n)), -2)
    thin = rng.random(n) < np.where(emp == "Gig/Platform", 0.25, 0.10) + np.where(age < 25, 0.08, 0.0)
    score = np.clip(np.round(rng.normal(715, 70, n) - np.where(emp == "Gig/Platform", 20, 0)), 300, 900)
    score = np.where(thin, np.nan, score)
    person = {"emp": emp, "age": age, "tier": tier, "income": income, "score": score,
              "emi_existing": np.where(rng.random(n) < 0.45, np.round(income * rng.uniform(0.05, 0.35, n), -2), 0.0),
              "enq": rng.poisson(1.5, n), "delinq": rng.poisson(np.where(np.nan_to_num(score, nan=650) > 700, 0.25, 0.7)),
              "util": np.round(np.clip(rng.beta(2, 3, n) * 1.2, 0, 1.2), 2), "u": rng.normal(0, 0.55, n)}
    d = {"date": dates}
    d = loan_level(rng, d, person)
    approved, z = decide(rng, d, person)
    # repeat applicants: 7.5% of rejected applications come back 20-90 days later with a smaller loan
    rej = np.flatnonzero(~approved & (D1 - dates > pd.Timedelta(days=100)))
    par = rng.choice(rej, size=int(0.075 * n), replace=False)
    m = len(par)
    cperson = {k: v[par].copy() for k, v in person.items()}
    cperson["income"] = np.round(cperson["income"] * rng.uniform(0.98, 1.08, m), -2)
    cperson["score"] = np.where(np.isnan(cperson["score"]), np.nan, np.clip(cperson["score"] + rng.integers(-15, 25, m), 300, 900))
    cd = {"date": dates[par] + pd.to_timedelta(rng.integers(20, 91, m), unit="D")}
    cd = loan_level(rng, cd, cperson)
    cd["loan_amount"] = np.clip(np.round(d["loan_amount"][par] * rng.uniform(0.55, 0.9, m) / 5000) * 5000, 20000, 1500000)
    new_emi = emi(cd["loan_amount"], cd["rate"], cd["tenure"]); cd["foir"] = np.round((cperson["emi_existing"] + new_emi) / cperson["income"], 3)
    capproved, cz = decide(rng, cd, cperson)
    # stack base + repeats
    allp = {k: np.concatenate([person[k], cperson[k]]) for k in person}
    alld = {k: np.concatenate([d[k], cd[k]]) for k in d}
    appr = np.concatenate([approved, capproved]); z_all = np.concatenate([z, cz])
    parent_id = np.concatenate([np.arange(n), par])
    N = len(appr)
    b0 = calibrate(z_all, appr, TARGET_DEFAULT_APPROVED)
    p_def = sigmoid(z_all + b0)
    default = rng.random(N) < p_def
    seen = appr.copy()
    noise = appr & default & (rng.random(N) < 0.01)                       # reporting lag: 1% of true defaults recorded as paid
    default_obs = np.where(seen, (default & ~noise).astype(float), np.nan)
    bounced = np.where(seen, (rng.random(N) < np.where(default, 0.55, 0.03)).astype(float), np.nan)
    dpd = np.where(seen, np.where(default, rng.integers(30, 181, N), np.where(rng.random(N) < 0.05, rng.integers(1, 30, N), 0)).astype(float), np.nan)
    calls = np.where(seen, np.where(default, rng.poisson(6, N), rng.poisson(0.2, N)).astype(float), np.nan)

    app_id = np.array([f"LA{9000000 + i}" for i in range(N)], dtype=object)
    applicant = np.array([f"AP{500000 + int(parent_id[i]) * 3 + 1}" for i in range(N)], dtype=object)
    truth = {"p_default": p_def.copy(), "approved": appr.copy(), "default_true": default.copy(), "noise": noise.copy(),
             "n_repeat_rows": m, "parent_id": parent_id.copy(), "emp": allp["emp"].copy(), "date": alld["date"], "thin": np.isnan(allp["score"]),
             "channel": alld["channel"].copy(), "intercept": float(b0)}
    order = np.argsort(alld["date"], kind="stable")
    df = pd.DataFrame({
        "application_id": app_id, "applicant_id": applicant, "application_date": alld["date"], "age": allp["age"].astype(float),
        "city_tier": allp["tier"], "employment_type": allp["emp"], "monthly_income_inr": allp["income"],
        "existing_emi_inr": allp["emi_existing"], "foir": alld["foir"], "bureau_score": allp["score"], "enquiries_6m": allp["enq"],
        "delinquencies_24m": allp["delinq"], "credit_utilisation": allp["util"], "loan_amount_inr": alld["loan_amount"],
        "tenure_months": alld["tenure"], "interest_rate_pct": alld["rate"], "purpose": alld["purpose"], "channel": alld["channel"],
        "approved": appr.astype(int), "default_12m": default_obs, "first_emi_bounced": bounced, "days_past_due_max_6m": dpd,
        "collections_calls": calls}).iloc[order].reset_index(drop=True)
    for k in ("p_default", "approved", "default_true", "noise", "parent_id", "emp", "thin", "channel"):
        truth[k] = truth[k][order]
    truth["date"] = alld["date"][order]
    # ---------- messiness
    m_ = len(df)
    date_txt = np.array([f"{t.year:04d}-{t.month:02d}-{t.day:02d}" for t in df["application_date"]], dtype=object)
    swap = rng.random(m_) < 0.04
    date_txt[swap] = [f"{t.day:02d}/{t.month:02d}/{t.year:04d}" for t in df["application_date"][swap]]
    df["application_date"] = date_txt
    inc_txt = df["monthly_income_inr"].map(lambda v: f"{v:.0f}").to_numpy(dtype=object)
    for i in np.flatnonzero(rng.random(m_) < 0.025):
        v = float(inc_txt[i]); k = int(rng.integers(0, 3))
        inc_txt[i] = f"{v / 1000:.0f}K" if k == 0 else (f"{v / 1e5:.1f}L" if k == 1 else f"{v:,.0f}")
    df["monthly_income_inr"] = inc_txt
    tier_v = df["city_tier"].to_numpy(dtype=object)
    for i in np.flatnonzero(rng.random(m_) < 0.04):
        tier_v[i] = {"Tier 1": "T1", "Tier 2": "tier 2", "Tier 3": "TIER-3"}[tier_v[i]]
    df["city_tier"] = tier_v
    a = df["age"].to_numpy(dtype=float).copy()
    a[rng.random(m_) < 0.01] = np.nan
    bad = rng.choice(np.flatnonzero(~np.isnan(a)), size=10, replace=False)
    a[bad] = np.array([5, 7, 120, 150, 0, 0, 999, 14, 16, 130], dtype=float)
    df["age"] = a
    ex = rng.choice(m_, size=40, replace=False)
    df = pd.concat([df, df.iloc[ex]], ignore_index=True)
    truth["n_dup_rows"] = 40
    return df, truth


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    out_dir = Path(args.out) if args.out else root / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    df, truth = generate()
    path = out_dir / "credit_loans.csv"
    o = df.copy()
    for c, nd in [("age", 0), ("bureau_score", 0), ("default_12m", 0), ("first_emi_bounced", 0), ("days_past_due_max_6m", 0), ("collections_calls", 0),
                  ("existing_emi_inr", 0), ("loan_amount_inr", 0), ("foir", 3), ("credit_utilisation", 2), ("interest_rate_pct", 1)]:
        o[c] = o[c].map(lambda v, nd=nd: "" if pd.isna(v) else f"{v:.{nd}f}")
    o.to_csv(path, index=False, lineterminator="\n")
    raw = path.read_bytes()
    ap_ = truth["approved"]
    print(f"credit_loans.csv: {len(df)} rows, {df.shape[1]} columns, {len(raw):,} bytes, sha256 {hashlib.sha256(raw).hexdigest()[:12]}")
    print(f"  approved {ap_.mean():.3f}; default among approved (true) {truth['default_true'][ap_].mean():.3f}; would-be default among rejected {truth['p_default'][~ap_].mean():.3f}")


if __name__ == "__main__":
    main()
