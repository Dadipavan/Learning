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
cat = orders.pivot_table(index="category", columns="quarter", values="amount", aggfunc="sum") / 1000
delta = (cat["Q2"] - cat["Q1"]).round(1)
start, end = cat["Q1"].sum().round(1), cat["Q2"].sum().round(1)
print(f"Q1 total {start} + changes {delta.sum().round(1)} = Q2 total {end}")
print(delta.to_string())
labels = ["Q1 total"] + list(delta.index) + ["Q2 total"]
values = [start] + delta.tolist() + [end]
fig, ax = plt.subplots(figsize=(8, 4.4))
running = start
ax.bar(0, start, color=GREY)
for i, d in enumerate(delta.tolist(), start=1):
    ax.bar(i, d, bottom=running, color=TEAL if d >= 0 else RED)
    ax.text(i, max(running, running + d) + 3, f"{d:+.1f}", ha="center", fontweight="bold")
    ax.plot([i - 0.7, i + 0.4], [running, running], color="#777", lw=0.8)
    running += d
ax.bar(len(delta) + 1, end, color=BLUE)
ax.text(0, start + 3, f"{start:.1f}", ha="center", fontweight="bold")
ax.text(len(delta) + 1, end + 3, f"{end:.1f}", ha="center", fontweight="bold")
ax.set_xticks(range(len(labels)), labels)
ax.set_ylim(100, 160)
ax.set_ylabel("Sales (Rs thousand)")
ax.set_title("Fashion and Grocery explain the Q2 drop")
fig.tight_layout()
fig.savefig("ch08v_waterfall.png", dpi=110)
print("saved")
