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
pivot = orders.pivot_table(index="city", columns="category", values="amount", aggfunc="sum") / 1000
pivot = pivot.loc[["Delhi", "Mumbai", "Pune"], ["Electronics", "Home", "Fashion", "Grocery"]]
print(pivot.round(1).to_string())
colors = [BLUE, TEAL, ORANGE, PURPLE]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.2), sharey=True)
width = 0.2
x = np.arange(len(pivot))
for i, cat in enumerate(pivot.columns):
    ax1.bar(x + (i - 1.5) * width, pivot[cat], width, color=colors[i], label=cat)
ax1.set_xticks(x, pivot.index); ax1.set_title("Grouped"); ax1.set_ylabel("Sales (Rs thousand)")
bottom = np.zeros(len(pivot))
for i, cat in enumerate(pivot.columns):
    ax2.bar(x, pivot[cat], 0.6, bottom=bottom, color=colors[i], label=cat)
    bottom += pivot[cat].to_numpy()
ax2.set_xticks(x, pivot.index); ax2.set_title("Stacked")
for xi, tot in zip(x, bottom): ax2.text(xi, tot + 2, f"{tot:.0f}", ha="center", fontweight="bold")
ax2.legend(frameon=False, loc="upper right")
fig.tight_layout()
fig.savefig("ch08v_grouped.png", dpi=110)
print("saved")
