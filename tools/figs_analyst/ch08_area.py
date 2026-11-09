import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
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
orders["month"] = orders["date"].dt.to_period("M").dt.to_timestamp()
cat_m = orders.pivot_table(index="month", columns="category", values="amount", aggfunc="sum") / 1000
cat_m = cat_m[["Electronics", "Home", "Fashion", "Grocery"]].round(1)
print(cat_m.to_string())
fig, ax = plt.subplots()
ax.stackplot(cat_m.index, cat_m.T.values, labels=cat_m.columns, colors=[BLUE, TEAL, ORANGE, PURPLE], alpha=0.95)
totals = cat_m.sum(axis=1)
for d, t in totals.items():
    ax.text(d, t + 1.2, f"{t:.0f}", ha="center", fontsize=11)
ax.set_xticks(cat_m.index, [d.strftime("%b") for d in cat_m.index])
ax.set_ylim(0, 62)
ax.set_ylabel("Sales (Rs thousand)")
ax.legend(frameon=False, loc="lower left", ncol=4, bbox_to_anchor=(0, 1.0), columnspacing=1.2)
ax.set_title("Electronics hit 31k in June while the rest shrank", pad=34)
fig.tight_layout()
fig.savefig("ch08v_area.png", dpi=110)
print("saved")
