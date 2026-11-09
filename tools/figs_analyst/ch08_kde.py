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
from scipy.stats import gaussian_kde
grid = np.linspace(0, 4500, 400)
colors = {"Electronics": BLUE, "Fashion": ORANGE, "Grocery": PURPLE}
fig, ax = plt.subplots()
for cat, color in colors.items():
    x = orders.loc[orders["category"] == cat, "amount"].to_numpy()
    dens = gaussian_kde(x)(grid)
    ax.plot(grid, dens, color=color, lw=2.5)
    ax.fill_between(grid, dens, color=color, alpha=0.12)
    peak_x = grid[dens.argmax()]
    ax.text(peak_x + 70, dens.max(), f"{cat} (n={len(x)})", color=color, va="bottom", fontweight="bold", fontsize=11)
    print(f"{cat:<12} n={len(x):>3}  median={np.median(x):>6.0f}  curve peaks near Rs {peak_x:.0f}")
ax.set_xlabel("Order amount (Rs)"); ax.set_ylabel("Density"); ax.set_yticks([])
ax.set_title("Grocery orders are small and tight; Electronics are big and varied")
ax.set_xlim(0, 4500)
fig.tight_layout()
fig.savefig("ch08v_kde.png", dpi=110)
print("saved")
