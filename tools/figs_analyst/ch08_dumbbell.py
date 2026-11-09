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
orders["quarter"] = np.where(orders["date"] < "2025-04-01", "Q1", "Q2")
aov = orders.pivot_table(index="category", columns="quarter", values="amount", aggfunc="mean").round(0)
aov = aov.sort_values("Q1")
aov["change_pct"] = ((aov["Q2"] / aov["Q1"] - 1) * 100).round(1)
print(aov.to_string())
fig, ax = plt.subplots()
y = np.arange(len(aov))
ax.hlines(y, aov["Q2"], aov["Q1"], color="#bbbbbb", lw=3, zorder=1)
ax.scatter(aov["Q1"], y, s=110, color=GREY, label="Q1 (Jan to Mar)", zorder=2)
ax.scatter(aov["Q2"], y, s=110, color=BLUE, label="Q2 (Apr to Jun)", zorder=2)
for yi, (q1, q2, pct) in enumerate(zip(aov["Q1"], aov["Q2"], aov["change_pct"])):
    ax.text(max(q1, q2) + 60, yi, f"{pct:+.0f}%", va="center", color=RED if pct < -10 else "#333")
ax.set_yticks(y, aov.index)
ax.set_xlim(0, 2400)
ax.set_xlabel("Average order value (Rs)")
ax.set_title("Fashion order value fell 21% in Q2")
ax.legend(frameon=False, loc="lower right")
fig.tight_layout()
fig.savefig("ch08v_dumbbell.png", dpi=110)
print("saved")
