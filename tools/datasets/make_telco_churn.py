#!/usr/bin/env python3
"""Generator for data/telco_churn.csv  (SPOILERS: this file contains the true generating rules).

A fictional Indian telecom operator: postpaid mobile customers, many with home broadband (fibre or 5G fixed wireless).
One row per customer at a snapshot date. Target: `churn` (did the customer leave in the next 90 days?).

Deterministic: fixed seed, numpy + pandas only, no clock. Run:  python3 tools/datasets/make_telco_churn.py [--out DIR]
"""
import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20250331
SNAPSHOT = pd.Timestamp("2025-03-31")
N_CUSTOMERS = 6500
TARGET_TRUE_CHURN = 0.265          # share of customers who truly leave (before label noise)
P_MISSED_PORTOUT = 0.03            # share of true churners whose label stayed "No" (port-out not yet recorded)
P_FALSE_CHURN = 0.007              # share of true stayers wrongly labelled "Yes" (billing-system clean-up)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# city -> (telecom circle, network-quality tickets multiplier)
CITIES = {
    "Mumbai": ("Maharashtra", 1.0), "Pune": ("Maharashtra", 0.9), "Nagpur": ("Maharashtra", 1.1),
    "Bengaluru": ("Karnataka", 0.9), "Mysuru": ("Karnataka", 1.0),
    "Chennai": ("Tamil Nadu", 0.9), "Coimbatore": ("Tamil Nadu", 1.0),
    "Delhi": ("Delhi NCR", 1.0), "Gurugram": ("Delhi NCR", 0.9), "Noida": ("Delhi NCR", 1.0),
    "Hyderabad": ("Telangana", 0.9), "Kolkata": ("West Bengal", 1.2),
    "Ahmedabad": ("Gujarat", 0.9), "Surat": ("Gujarat", 1.0),
    "Lucknow": ("Uttar Pradesh", 1.5), "Kanpur": ("Uttar Pradesh", 1.7), "Agra": ("Uttar Pradesh", 1.6),
    "Jaipur": ("Rajasthan", 1.2), "Kochi": ("Kerala", 0.9), "Chandigarh": ("Punjab", 1.0),
}
CITY_P = [0.15, 0.07, 0.03, 0.13, 0.02, 0.08, 0.02, 0.10, 0.04, 0.04, 0.07, 0.05, 0.04, 0.02, 0.02, 0.01, 0.01, 0.03, 0.02, 0.02]
CITY_VARIANTS = {
    "Bengaluru": ["Bangalore", "bangalore", "BENGALURU", "Bengaluru "],
    "Mumbai": ["Bombay", "mumbai", "MUMBAI"],
    "Delhi": ["New Delhi", "delhi", "DELHI", "Delhi NCR"],
    "Chennai": ["Madras", "chennai"],
    "Kolkata": ["Calcutta", "kolkata"],
    "Gurugram": ["Gurgaon", "gurugram"],
    "Pune": ["pune", "PUNE"],
    "Hyderabad": ["hyderabad", "Hydrabad"],
}

PAYMENT = ["UPI AutoPay", "Credit card auto-debit", "NACH e-mandate", "Net banking", "Cash at store"]
PAYMENT_P = [0.34, 0.20, 0.14, 0.17, 0.15]
PAY_EFFECT = {"UPI AutoPay": -0.35, "Credit card auto-debit": -0.30, "NACH e-mandate": -0.20, "Net banking": 0.15, "Cash at store": 0.60}
LATE_RATE = {"UPI AutoPay": 0.15, "Credit card auto-debit": 0.15, "NACH e-mandate": 0.2, "Net banking": 0.5, "Cash at store": 0.9}
CONTRACT_EFFECT = {"Month-to-month": 0.95, "1 year": -0.30, "2 year": -1.40}
TIERS = ["Basic 349", "Standard 499", "Premium 699", "Max 999"]
TIER_PRICE = np.array([349, 499, 699, 999])
TIER_DATA_MEDIAN = np.array([6.0, 13.0, 26.0, 50.0])
REASONS = ["Better offer from competitor", "Network quality", "Price too high", "Poor customer service",
           "Relocation", "Moved to prepaid", "Other"]
REASON_P = [0.28, 0.22, 0.20, 0.12, 0.08, 0.06, 0.04]

COEF_REPORT = {  # for the answer key (log-odds)
    "contract_month_to_month": 0.95, "contract_1_year": -0.30, "contract_2_year": -1.40,
    "tenure_per_month_up_to_48": -0.035, "support_calls_per_call_cap6": 0.32, "network_tickets_per_ticket_cap5": 0.20,
    "late_payments_per_payment_cap4": 0.40, "cash_at_store": 0.60, "upi_autopay": -0.35,
    "paperless_billing": 0.20, "price_vs_usage_gap_per_sd": 0.45, "age_under_26": 0.35, "age_62_plus": 0.25,
    "married": -0.30, "dependents": -0.20, "extra_line_each": -0.22, "unobserved_noise_sd": 0.6,
}


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def calibrate_intercept(z, target):
    lo, hi = -10.0, 10.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if sigmoid(z + mid).mean() > target:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def fmt_dates(dates, styles):
    out = []
    for d, s in zip(dates, styles):
        if s == 0:
            out.append(f"{d.year:04d}-{d.month:02d}-{d.day:02d}")
        elif s == 1:
            out.append(f"{d.day:02d}/{d.month:02d}/{d.year:04d}")
        elif s == 2:
            out.append(f"{d.day:02d}-{MONTHS[d.month - 1]}-{d.year:04d}")
        else:
            out.append(f"{MONTHS[d.month - 1]} {d.day}, {d.year}")
    return out


def zscore(x):
    return (x - x.mean()) / x.std()


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    n = N_CUSTOMERS

    # ---------------- tenure and signup date (ids are assigned in signup order)
    u = rng.random(n)
    tenure_days = np.where(u < 0.008, rng.uniform(0, 30, n),
                           np.where(u < 0.32, 30 + rng.exponential(220, n), rng.uniform(150, 2500, n)))
    tenure_days = np.floor(np.minimum(tenure_days, 2600)).astype(int)
    order = np.argsort(-tenure_days, kind="stable")          # oldest customer first
    tenure_days = tenure_days[order]
    signup = SNAPSHOT - pd.to_timedelta(tenure_days, unit="D")
    tenure_months = np.floor(tenure_days / 30.4375).astype(int)
    ids = 100001 + np.cumsum(rng.integers(1, 4, n))
    customer_id = np.array([f"TC-{i}" for i in ids])

    # ---------------- demographics
    age = np.clip(np.round(rng.normal(36, 12, n)), 18, 82).astype(int)
    gender = np.where(rng.random(n) < 0.58, "Male", "Female")
    p_married = sigmoid((age - 28) / 5.0) * 0.85
    married = rng.random(n) < p_married
    dependents = rng.random(n) < np.where(married, 0.55, 0.12)
    lines = np.where(rng.random(n) < 0.62, 1, rng.choice([2, 3, 4], size=n, p=[0.5, 0.3, 0.2]))
    lines = np.where(married & (lines == 1) & (rng.random(n) < 0.35), 2, lines)

    city_names = list(CITIES)
    city = rng.choice(city_names, size=n, p=np.array(CITY_P) / np.sum(CITY_P))
    circle = np.array([CITIES[c][0] for c in city])
    net_mult = np.array([CITIES[c][1] for c in city])

    # ---------------- plan, internet, add-ons
    tier = rng.choice(4, size=n, p=[0.30, 0.35, 0.22, 0.13])
    p_fibre = 0.24 + 0.09 * tier
    r = rng.random(n)
    internet = np.where(r < p_fibre, "Fibre", np.where(r < p_fibre + 0.17, "5G Home", "None"))
    fibre_price = rng.choice([399, 599, 999], size=n, p=[0.45, 0.40, 0.15])
    fwa_price = rng.choice([499, 799], size=n, p=[0.6, 0.4])
    internet_price = np.where(internet == "Fibre", fibre_price, np.where(internet == "5G Home", fwa_price, 0))
    ott = np.where(internet == "None", "No internet service", np.where(rng.random(n) < 0.45, "Yes", "No"))
    dev_prot = np.where(rng.random(n) < 0.25, "Yes", "No")

    # contract depends on tenure
    p_m2m = np.where(tenure_months < 12, 0.78, np.where(tenure_months < 36, 0.50, 0.32))
    r = rng.random(n)
    contract = np.where(r < p_m2m, "Month-to-month",
                        np.where(r < p_m2m + (1 - p_m2m) * 0.45, "1 year", "2 year"))

    payment = rng.choice(PAYMENT, size=n, p=PAYMENT_P)
    paperless = np.where(rng.random(n) < np.where(np.isin(payment, ["UPI AutoPay", "Credit card auto-debit"]), 0.75, 0.45), "Yes", "No")

    # ---------------- usage and bill
    data_median = TIER_DATA_MEDIAN[tier] * np.exp(-0.012 * (age - 36))
    data_gb = np.round(np.exp(rng.normal(np.log(data_median), 0.85)), 1)
    calls = np.round(np.exp(rng.normal(np.log(280) + 0.008 * (age - 36), 0.7))).astype(int)
    calls = np.where(rng.random(n) < 0.03, 0, calls)
    promo = np.where(rng.random(n) < 0.15, 0.90, 1.0)
    base = TIER_PRICE[tier] + (lines - 1) * 199 + internet_price + np.where(ott == "Yes", 199, 0) + np.where(dev_prot == "Yes", 99, 0)
    monthly = np.round(base * 1.18 * promo, 2)          # includes 18% GST

    late = rng.poisson(np.array([LATE_RATE[p] for p in payment]))
    tickets = rng.poisson(0.35 * net_mult * np.where(internet == "5G Home", 1.4, 1.0))
    support_mu = 0.55 + 0.35 * np.minimum(tickets, 4) + 0.2 * (late > 0)
    support_calls = rng.poisson(rng.gamma(1.5, support_mu / 1.5))

    # ---------------- the true churn model (log-odds)
    value_gap = zscore(np.log(monthly)) - zscore(np.log(data_gb + 1.0))
    z = np.array([CONTRACT_EFFECT[c] for c in contract])
    z = z - 0.035 * np.minimum(tenure_months, 48)
    z = z + 0.32 * np.minimum(support_calls, 6) + 0.20 * np.minimum(tickets, 5) + 0.40 * np.minimum(late, 4)
    z = z + np.array([PAY_EFFECT[p] for p in payment]) + np.where(paperless == "Yes", 0.20, 0.0)
    z = z + 0.45 * value_gap
    z = z + np.where((internet == "Fibre") & (ott == "No"), 0.30, 0.0) + np.where(internet == "5G Home", 0.25, 0.0)
    z = z + np.where(age < 26, 0.35, 0.0) + np.where(age >= 62, 0.25, 0.0)
    z = z - 0.30 * married - 0.20 * dependents - 0.22 * (lines - 1)
    z = z + rng.normal(0, 0.6, n)
    b0 = calibrate_intercept(z, TARGET_TRUE_CHURN)
    p_churn = sigmoid(z + b0)
    churn_true = rng.random(n) < p_churn

    # ---------------- observed label with noise, and the two leaky columns
    flip_to_no = np.zeros(n, dtype=bool)                          # exact counts, so the documented rates are exact
    yes_idx, no_idx = np.flatnonzero(churn_true), np.flatnonzero(~churn_true)
    flip_to_no[rng.choice(yes_idx, size=int(round(P_MISSED_PORTOUT * len(yes_idx))), replace=False)] = True
    flip_to_yes = np.zeros(n, dtype=bool)
    flip_to_yes[rng.choice(no_idx, size=int(round(P_FALSE_CHURN * len(no_idx))), replace=False)] = True
    churn_obs = (churn_true & ~flip_to_no) | flip_to_yes
    reason = np.where(rng.random(n) < 0.90, rng.choice(REASONS, size=n, p=REASON_P), "")
    reason = np.where(churn_true, reason, "")                       # recorded from the TRUE event, so flip_to_no rows keep one
    winback = np.where(churn_true, rng.random(n) < 0.85, rng.random(n) < 0.015)
    winback = np.where(winback, "Yes", "No")

    # ---------------- total charges (text) : blank for customers not yet billed
    drift = rng.uniform(0.85, 1.05, n)
    total = np.round(monthly * tenure_months * drift, 2)

    # ================= messiness (applied after the truth is fixed)
    df = pd.DataFrame({
        "customer_id": customer_id, "signup_date": signup, "city": city, "circle": circle, "gender": gender,
        "age": age.astype(float), "married": np.where(married, "Yes", "No"), "dependents": np.where(dependents, "Yes", "No"),
        "tenure_months": tenure_months, "contract": contract, "plan_tier": np.array(TIERS)[tier], "num_lines": lines,
        "internet_service": internet, "ott_bundle": ott, "device_protection": dev_prot,
        "monthly_data_gb": data_gb, "monthly_call_minutes": calls, "support_calls_90d": support_calls,
        "network_tickets_90d": tickets, "late_payments_6m": late, "payment_method": payment,
        "paperless_billing": paperless, "monthly_charges": monthly, "total_charges": total,
        "churn": np.where(churn_obs, "Yes", "No"), "cancellation_reason": reason, "winback_offer_sent": winback,
    })
    truth = {"churn_true": churn_true.copy(), "flip_to_no": flip_to_no.copy(), "flip_to_yes": flip_to_yes.copy(),
             "intercept": float(b0), "p_churn": p_churn.copy(), "tenure_months": tenure_months.copy(),
             "age_true": age.copy(), "data_gb_true": data_gb.copy(), "coef": COEF_REPORT}

    # -- inconsistent city spellings (about 9%) and trailing blanks
    city_col = df["city"].to_numpy(dtype=object).copy()
    dirty = rng.random(n) < 0.09
    for i in np.flatnonzero(dirty):
        opts = CITY_VARIANTS.get(city_col[i])
        if opts:
            city_col[i] = opts[int(rng.integers(0, len(opts)))]
    df["city"] = city_col

    # -- contract spelling variants (5%)
    c_col = df["contract"].to_numpy(dtype=object).copy()
    alt = {"Month-to-month": ["Month to Month", "month-to-month", "Monthly"], "1 year": ["One year", "1 Year"], "2 year": ["Two year", "2 Year"]}
    for i in np.flatnonzero(rng.random(n) < 0.05):
        opts = alt[c_col[i]]
        c_col[i] = opts[int(rng.integers(0, len(opts)))]
    df["contract"] = c_col

    # -- MCAR blanks: gender 3%, circle 2%
    g = df["gender"].to_numpy(dtype=object).copy()
    g[rng.random(n) < 0.03] = ""
    df["gender"] = g
    cc = df["circle"].to_numpy(dtype=object).copy()
    cc[rng.random(n) < 0.02] = ""
    df["circle"] = cc

    # -- MAR blanks: age is missing far more often for cash-at-store customers (retailer-activated SIMs)
    age_f = df["age"].to_numpy(dtype=float).copy()
    miss_age = rng.random(n) < np.where(payment == "Cash at store", 0.09, 0.012)
    age_f[miss_age] = np.nan
    # placeholder zeros and impossible ages
    zero_idx = rng.choice(np.flatnonzero(~miss_age), size=18, replace=False)
    age_f[zero_idx] = 0
    left = np.setdiff1d(np.flatnonzero(~miss_age), zero_idx)
    big_idx = rng.choice(left, size=6, replace=False)
    age_f[big_idx] = np.array([118, 150, 999, 121, 124, 130], dtype=float)
    df["age"] = age_f

    # -- MNAR blanks: very low data usage (< 2.5 GB) is often recorded as blank (meter wrote nothing), plus 1% MCAR
    d_f = df["monthly_data_gb"].to_numpy(dtype=float).copy()
    miss_data = rng.random(n) < np.where(data_gb < 2.5, 0.40, 0.010)
    d_f[miss_data] = np.nan
    sent_idx = rng.choice(np.flatnonzero(~miss_data), size=13, replace=False)
    d_f[sent_idx] = 9999.0                                        # sentinel meaning "meter error"
    df["monthly_data_gb"] = d_f

    # -- unit errors in monthly_charges: paise instead of rupees (x100), and credit-note negatives
    m_f = df["monthly_charges"].to_numpy(dtype=float).copy()
    pick = rng.choice(n, size=14, replace=False)
    m_f[pick[:8]] = np.round(m_f[pick[:8]] * 100, 2)
    m_f[pick[8:]] = -m_f[pick[8:]]
    df["monthly_charges"] = m_f

    # -- tenure that disagrees with the signup date (0.5%)
    t_f = df["tenure_months"].to_numpy(dtype=int).copy()
    pick = rng.choice(np.flatnonzero(t_f > 6), size=int(0.005 * n), replace=False)
    t_f[pick] = t_f[pick] + rng.integers(9, 25, size=len(pick))
    df["tenure_months"] = t_f

    # -- total_charges as text: " " for customers with 0 months, thousands separators for 1%
    tot = []
    comma = rng.random(n) < 0.012
    for i in range(n):
        if tenure_months[i] == 0:
            tot.append(" ")
        elif comma[i] and total[i] >= 1000:
            tot.append(f"{total[i]:,.2f}")
        else:
            tot.append(f"{total[i]:.2f}")
    df["total_charges"] = tot

    # -- signup_date in four text formats (76/14/6/4 %)
    styles = rng.choice(4, size=n, p=[0.76, 0.14, 0.06, 0.04])
    df["signup_date"] = fmt_dates(df["signup_date"], styles)

    # -- duplicates: two extracts were appended (exact copies) and a re-keyed batch from a CRM clean-up
    n_exact, n_rekey = 70, 25
    pick = rng.choice(n, size=n_exact + n_rekey, replace=False)
    exact = df.iloc[pick[:n_exact]].copy()
    rekey = df.iloc[pick[n_exact:]].copy()
    rekey["customer_id"] = [("tc-" + cid[3:]) if k % 2 == 0 else (" " + cid + " ") for k, cid in enumerate(rekey["customer_id"])]
    df = pd.concat([df, exact, rekey], ignore_index=True)
    truth["n_exact_dups"] = n_exact
    truth["n_rekey_dups"] = n_rekey
    truth["n_unique_customers"] = n
    truth["dup_source_index"] = pick.copy()
    return df, truth


def fmt_table(df):
    out = df.copy()
    for c in ["age", "monthly_data_gb"]:
        out[c] = out[c].map(lambda v: "" if pd.isna(v) else (f"{v:.1f}" if c == "monthly_data_gb" else f"{int(v)}"))
    out["monthly_charges"] = out["monthly_charges"].map(lambda v: f"{v:.2f}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="output folder (default: <repo>/data)")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    out_dir = Path(args.out) if args.out else root / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    df, truth = generate()
    path = out_dir / "telco_churn.csv"
    fmt_table(df).to_csv(path, index=False, lineterminator="\n")
    raw = path.read_bytes()
    first = df.iloc[: truth["n_unique_customers"]]
    print(f"telco_churn.csv: {len(df)} rows, {df.shape[1]} columns, {len(raw):,} bytes, sha256 {hashlib.sha256(raw).hexdigest()[:12]}")
    print(f"  true churn rate {truth['churn_true'].mean():.3f}; observed 'Yes' {(first['churn'] == 'Yes').mean():.3f}; "
          f"duplicates added: {truth['n_exact_dups']} exact + {truth['n_rekey_dups']} re-keyed")


if __name__ == "__main__":
    main()
