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
mum = orders[orders["city"] == "Mumbai"]
cat = (mum.pivot_table(index="category", columns="quarter", values="amount", aggfunc="sum") / 1000)
delta = (cat["Q2"] - cat["Q1"]).sort_values()
share = delta.min() / delta.sum()
cnt = mum.groupby("quarter").size()
avg = mum.groupby("quarter")["amount"].mean()
print(delta.round(1).to_string())
print(f"Electronics share of Mumbai's fall: {share:.0%}")
print(f"Mumbai orders {cnt['Q1']} -> {cnt['Q2']} ({cnt['Q2'] / cnt['Q1'] - 1:+.0%}); average order {avg['Q1']:.0f} -> {avg['Q2']:.0f} ({avg['Q2'] / avg['Q1'] - 1:+.0%})")
fig, ax = plt.subplots(figsize=(8, 4.5))
cols = [ORANGE if c == delta.idxmin() else "#e6c3b3" for c in delta.index]
bars = ax.barh(delta.index, delta.values, color=cols, height=0.6)
for bar, v in zip(bars, delta.values):
    ax.text(v - 0.5, bar.get_y() + bar.get_height() / 2, f"{v:.1f}k", ha="right", va="center", fontsize=14, fontweight="bold")
ax.set_xlim(-19, 1); ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
ax.yaxis.tick_right(); ax.tick_params(axis="y", length=0, labelsize=14)
fig.suptitle(f"Electronics explains {share:.0%} of Mumbai's Q2 fall", x=0.02, ha="left", fontsize=17, fontweight="bold")
fig.text(0.02, 0.855, "Mumbai: change in sales by category, Q2 minus Q1, Rs thousand", fontsize=12, color="#555")
fig.text(0.02, 0.26, f"Next step: check Mumbai Electronics stock and pricing. Orders fell {abs(cnt['Q2'] / cnt['Q1'] - 1):.0%} and\n"
         f"the average order fell {abs(avg['Q2'] / avg['Q1'] - 1):.0%}, so both volume and basket size need an answer.",
         fontsize=12, color="#222", bbox=dict(boxstyle="round,pad=0.5", fc="#f3f5fc", ec=BLUE), va="top")
fig.text(0.02, 0.02, "Source: orders table (synthetic, seed 8)", fontsize=9.5, color="#666")
fig.text(0.98, 0.02, "3 of 3", fontsize=9.5, color="#666", ha="right")
fig.subplots_adjust(left=0.04, right=0.80, top=0.8, bottom=0.36)
fig.savefig("ch08v_story3.png", dpi=110)
print("saved")
