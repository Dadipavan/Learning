import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd

rng = np.random.default_rng(8)
n = 300
category = rng.choice(["Electronics", "Home", "Fashion", "Grocery"], n, p=[0.2, 0.25, 0.3, 0.25])
mu = pd.Series({"Electronics": 7.4, "Home": 6.8, "Fashion": 6.4, "Grocery": 5.6})[category].to_numpy()
orders = pd.DataFrame({
    "date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 180, n), unit="D"),
    "city": rng.choice(["Delhi", "Mumbai", "Pune"], n, p=[0.40, 0.35, 0.25]),
    "category": category,
    "channel": rng.choice(["App", "Web"], n, p=[0.6, 0.4]),
    "amount": np.round(rng.lognormal(mu, 0.6)).astype(int)})
orders["month"] = orders["date"].dt.to_period("M").dt.to_timestamp()
orders["quarter"] = np.where(orders["date"] < "2025-04-01", "Q1", "Q2")

kpi = {"sales": orders["amount"].sum(), "orders": len(orders), "avg_order": orders["amount"].mean(),
       "q2_vs_q1": orders.loc[orders.quarter == "Q2", "amount"].sum() / orders.loc[orders.quarter == "Q1", "amount"].sum() - 1}
monthly = orders.groupby("month")["amount"].sum().div(1000).round(1)
by_city = orders.groupby("city")["amount"].sum().div(1000).sort_values().round(1)
by_cat = orders.groupby("category")["amount"].mean().sort_values().round(0)
print({k: round(float(v), 3) for k, v in kpi.items()})
print(monthly.rename_axis(None).rename(lambda d: d.strftime("%b")).to_string())
print(by_city.to_string())
print(by_cat.to_string())
print("shapes:", monthly.shape, by_city.shape, by_cat.shape, orders["amount"].shape)
