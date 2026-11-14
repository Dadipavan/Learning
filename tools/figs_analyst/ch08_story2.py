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
city = (orders.pivot_table(index="city", columns="quarter", values="amount", aggfunc="sum") / 1000)
delta = (city["Q2"] - city["Q1"]).sort_values()
print(delta.round(1).to_string())
print(f"total change {delta.sum():.1f}k")
colors = {"Delhi": BLUE, "Mumbai": ORANGE, "Pune": GREY}
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(delta.index, delta.values, color=[colors[c] for c in delta.index], height=0.6)
for bar, v in zip(bars, delta.values):
    ax.text(v + (0.8 if v > 0 else -0.8), bar.get_y() + bar.get_height() / 2, f"{v:+.1f}k",
            ha="left" if v > 0 else "right", va="center", fontsize=14, fontweight="bold")
ax.axvline(0, color="#333", lw=1)
ax.set_xlim(-34, 28); ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0, labelsize=14)
fig.suptitle(f"Mumbai lost Rs {abs(delta['Mumbai']):.1f}k, more than Delhi gained (Rs {delta['Delhi']:.1f}k)",
             x=0.02, ha="left", fontsize=17, fontweight="bold")
fig.text(0.02, 0.855, "Change in sales, Q2 minus Q1, Rs thousand", fontsize=12, color="#555")
fig.text(0.02, 0.02, "Source: orders table (synthetic, seed 8)", fontsize=9.5, color="#666")
fig.text(0.98, 0.02, "2 of 3", fontsize=9.5, color="#666", ha="right")
fig.subplots_adjust(left=0.12, right=0.98, top=0.8, bottom=0.12)
fig.savefig("ch08v_story2.png", dpi=110)
print("saved")
