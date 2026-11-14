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
cat_m = (orders.pivot_table(index="month", columns="category", values="amount", aggfunc="sum") / 1000).round(1)
rows = cat_m.columns.tolist()
fig, axs = plt.subplots(len(rows), 1, figsize=(8, 3.6))
for ax, name in zip(axs, rows):
    s = cat_m[name]
    ax.plot(range(len(s)), s.values, color=GREY, lw=2)
    ax.scatter([s.values.argmax(), len(s) - 1], [s.max(), s.iloc[-1]], color=[BLUE, RED], zorder=3, s=30)
    ax.axis("off")
    change = (s.iloc[-1] / s.iloc[0] - 1) * 100
    ax.text(-0.9, s.mean(), name, ha="right", va="center", fontweight="bold")
    ax.text(len(s) - 0.4, s.mean(), f"Jun {s.iloc[-1]:.1f}k   ({change:+.0f}% vs Jan)", va="center")
    ax.set_xlim(-0.2, len(s) + 3.5)
    ax.margins(y=0.3)
fig.suptitle("Monthly sales by category, Jan to Jun (blue = best month, red = latest)", x=0.02, ha="left", fontweight="bold", fontsize=13)
fig.subplots_adjust(left=0.2, right=0.98, top=0.86, bottom=0.02, hspace=0.35)
fig.savefig("ch08v_sparkline.png", dpi=110)
print(cat_m.iloc[[0, -1]].to_string())
print("saved")
