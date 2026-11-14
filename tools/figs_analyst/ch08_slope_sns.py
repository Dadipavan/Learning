import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="white", font_scale=1.1, rc={"figure.figsize": (8, 4.2), "figure.dpi": 110,
              "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
              "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
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
orders["quarter"] = np.where(orders["date"] < "2025-04-01", "Q1", "Q2")
long = orders.groupby(["city", "quarter"], as_index=False)["amount"].sum()
long["amount"] = long["amount"] / 1000
ax = sns.lineplot(data=long, x="quarter", y="amount", hue="city", marker="o", markersize=9, linewidth=3,
                  palette={"Delhi": BLUE, "Mumbai": ORANGE, "Pune": GREY})
ax.set(xlabel="", ylabel="Sales (Rs thousand)", title="Delhi overtook Mumbai in Q2", xlim=(-0.2, 1.2))
sns.move_legend(ax, "upper left", frameon=False, bbox_to_anchor=(1, 1))
ax.figure.tight_layout()
ax.figure.savefig("ch08v_slope_sns.png", dpi=110)
print(long.round(1).to_string(index=False))
print("saved")
