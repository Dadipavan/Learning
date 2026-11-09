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
cat_m = (orders.pivot_table(index="month", columns="category", values="amount", aggfunc="sum") / 1000)
cat_m = cat_m[["Electronics", "Home", "Fashion", "Grocery"]]
print(cat_m.round(1).agg(["min", "max"]).to_string())
x = np.arange(len(cat_m))
fig, axs = plt.subplots(2, 2, figsize=(8, 5), sharex=True, sharey=True)
for ax, cat in zip(axs.ravel(), cat_m.columns):
    for other in cat_m.columns:
        ax.plot(x, cat_m[other], color="#dddddd", lw=1.5)               # all categories as faint context
    ax.plot(x, cat_m[cat], color=BLUE, lw=3)                           # this panel's category on top
    ax.set_title(cat, fontsize=12)
    ax.set_xticks(x, [d.strftime("%b") for d in cat_m.index])
for ax in axs[:, 0]: ax.set_ylabel("Sales (Rs thousand)")
fig.suptitle("Electronics swings most; Grocery stays small", x=0.01, ha="left", fontweight="bold", fontsize=14)
fig.tight_layout()
fig.savefig("ch08v_smallmult.png", dpi=110)
print("saved")
