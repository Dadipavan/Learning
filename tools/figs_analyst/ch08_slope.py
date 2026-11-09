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
city = (orders.pivot_table(index="city", columns="quarter", values="amount", aggfunc="sum") / 1000).round(1)
city["change_pct"] = ((city["Q2"] / city["Q1"] - 1) * 100).round(1)
print(city.to_string())
colors = {"Delhi": BLUE, "Mumbai": ORANGE, "Pune": GREY}
fig, ax = plt.subplots(figsize=(6.5, 4.4))
for name, row in city.iterrows():
    ax.plot([0, 1], [row["Q1"], row["Q2"]], color=colors[name], marker="o", lw=3, ms=8)
    tc = "#666666" if name == "Pune" else colors[name]          # darker grey text for contrast
    ax.text(-0.04, row["Q1"], f"{name}  {row['Q1']:.1f}", ha="right", va="center", color=tc)
    ax.text(1.04, row["Q2"], f"{row['Q2']:.1f}  ({row['change_pct']:+.0f}%)", ha="left", va="center", color=tc)
ax.set_xlim(-0.55, 1.6); ax.set_ylim(10, 75)
ax.set_xticks([0, 1], ["Q1 (Jan to Mar)", "Q2 (Apr to Jun)"])
ax.set_yticks([])
ax.spines[["left", "bottom"]].set_visible(False)
ax.tick_params(length=0)
ax.set_title("Delhi overtook Mumbai in Q2", loc="center")
fig.tight_layout()
fig.savefig("ch08v_slope.png", dpi=110)
print("saved")
