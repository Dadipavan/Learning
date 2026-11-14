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
order = ["Electronics", "Home", "Fashion", "Grocery"]
colors = [BLUE, TEAL, ORANGE, PURPLE]
data = [np.log10(orders.loc[orders["category"] == c, "amount"]) for c in order]
print(orders.groupby("category")["amount"].median().loc[order].to_string())
ticks = np.log10([100, 300, 1000, 3000]); ticklabels = ["100", "300", "1,000", "3,000"]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4), sharey=True)
bp = ax1.boxplot(data, orientation="horizontal", tick_labels=order, patch_artist=True, widths=0.6,
                 medianprops=dict(color="white", lw=2.5), flierprops=dict(marker="o", ms=4, mfc="none", mec="#555"))
for patch, color in zip(bp["boxes"], colors): patch.set(facecolor=color, edgecolor=color)
ax1.set_title("Box plot")
vp = ax2.violinplot(data, orientation="horizontal", showmedians=True, showextrema=False)
for body, color in zip(vp["bodies"], colors): body.set(facecolor=color, alpha=0.8)
vp["cmedians"].set(color="white", lw=2.5)
ax2.set_title("Violin plot")
for ax in (ax1, ax2):
    ax.set_xticks(ticks, ticklabels); ax.set_xlabel("Order amount (Rs, log scale)")
ax1.invert_yaxis()
fig.tight_layout()
fig.savefig("ch08v_boxviolin.png", dpi=110)
print("saved")
