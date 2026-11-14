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
orders["quarter"] = np.where(orders["date"] < "2025-04-01", "Q1", "Q2")
m = orders.groupby("month")["amount"].sum() / 1000
q = orders.groupby("quarter")["amount"].sum() / 1000
change = q["Q2"] / q["Q1"] - 1
print(m.round(1).to_string())
print(f"Q1 {q['Q1']:.1f}k, Q2 {q['Q2']:.1f}k, change {change:+.1%}")
fig, ax = plt.subplots(figsize=(8, 4.5))
colors = [GREY] * 3 + [BLUE] * 3
bars = ax.bar([d.strftime("%b") for d in m.index], m.values, color=colors, width=0.62)
ax.bar_label(bars, labels=[f"{v:.0f}" for v in m.values], padding=3, fontsize=12)
for x0, label in [(1, f"Q1: Rs {q['Q1']:.1f}k"), (4, f"Q2: Rs {q['Q2']:.1f}k")]:
    ax.text(x0, 66, label, ha="center", fontsize=13, fontweight="bold", color="#333" if x0 == 1 else BLUE)
ax.set_ylim(0, 72); ax.set_yticks([]); ax.spines["left"].set_visible(False)
fig.suptitle(f"Sales fell {abs(change):.0%} from Q1 to Q2", x=0.02, ha="left", fontsize=17, fontweight="bold")
fig.text(0.02, 0.855, "Monthly sales, Rs thousand, Jan to Jun 2025", fontsize=12, color="#555")
fig.text(0.02, 0.02, "Source: orders table (synthetic, seed 8)", fontsize=9.5, color="#666")
fig.text(0.98, 0.02, "1 of 3", fontsize=9.5, color="#666", ha="right")
fig.subplots_adjust(left=0.05, right=0.98, top=0.8, bottom=0.12)
fig.savefig("ch08v_story1.png", dpi=110)
print("saved")
