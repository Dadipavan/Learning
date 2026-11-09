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
grid = orders.pivot_table(index="category", columns="city", values="amount", aggfunc="mean").loc[order, ["Delhi", "Mumbai", "Pune"]].round(0)
print(grid.to_string())
fig, ax = plt.subplots(figsize=(7, 4))
im = ax.imshow(grid.values, cmap="Blues", vmin=0, vmax=2500)
ax.set_xticks(range(3), grid.columns); ax.set_yticks(range(4), grid.index)
ax.xaxis.tick_top(); ax.tick_params(length=0)
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        v = grid.values[i, j]
        ax.text(j, i, f"{v:,.0f}", ha="center", va="center", fontsize=13, fontweight="bold",
                color="white" if v > 1250 else "#222")
for s in ax.spines.values(): s.set_visible(False)
cb = fig.colorbar(im, ax=ax, shrink=0.85); cb.set_label("Average order (Rs)")
fig.suptitle("Electronics orders are biggest in Delhi and Mumbai", x=0.02, ha="left", fontweight="bold", fontsize=14)
fig.tight_layout()
fig.savefig("ch08v_heatmap.png", dpi=110)
print("saved")
