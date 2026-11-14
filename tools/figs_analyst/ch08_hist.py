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
amt = orders["amount"]
print(amt.describe().round(0).to_string())
print(f"share under Rs 1,000: {(amt < 1000).mean():.0%} | mean {amt.mean():.0f} | median {amt.median():.0f}")
for width in (50, 200, 1000, 3000):
    counts, _ = np.histogram(amt, bins=np.arange(0, amt.max() + width, width))
    print(f"bin width {width:>4}: {len(counts):>3} bins, tallest bin holds {counts.max()} orders")
fig, ax = plt.subplots()
ax.hist(amt, bins=np.arange(0, 5800, 200), color=BLUE, edgecolor="white")
ax.axvline(amt.median(), color=ORANGE, lw=2.5)
ax.axvline(amt.mean(), color=RED, lw=2.5, ls="--")
ax.annotate(f"median {amt.median():,.0f}", xy=(amt.median(), 54), xytext=(1900, 54), color=ORANGE, va="center",
            fontweight="bold", arrowprops=dict(arrowstyle="-", color=ORANGE))
ax.annotate(f"mean {amt.mean():,.0f}", xy=(amt.mean(), 45), xytext=(1900, 45), color=RED, va="center",
            fontweight="bold", arrowprops=dict(arrowstyle="-", color=RED))
ax.set_xlabel("Order amount (Rs)"); ax.set_ylabel("Number of orders")
ax.set_title("Most orders are small; a few big ones pull the mean up")
fig.tight_layout()
fig.savefig("ch08v_hist.png", dpi=110)
print("saved")
