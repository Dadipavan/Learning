import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
months = pd.period_range("2024-01", "2025-06", freq="M").to_timestamp()
monthly = pd.Series([310, 295, 340, 360, 385, 400, 380, 410, 430, 470, 560, 620,
                     350, 330, 375, 405, 430, 455], index=months, name="sales_k")
fig, axs = plt.subplots(1, 3, figsize=(11, 3.8), layout="constrained")
windows = [("Nov 2024 to Jan 2025", "2024-11", "2025-01", RED), ("Jan to Oct 2024", "2024-01", "2024-10", ORANGE), ("All 18 months", "2024-01", "2025-06", BLUE)]
titles = ["'Sales crashed'", "'Steady growth'", "The honest picture"]
for ax, (label, a, b, color), title in zip(axs, windows, titles):
    s = monthly.loc[a:b]
    ax.plot(s.index, s.values, color=color, lw=2.8, marker="o", ms=4)
    ax.set_title(title, fontsize=13); ax.set_xlabel(label)
    ax.set_xticks(s.index[::max(1, len(s) // 4)], [d.strftime("%b %y") for d in s.index[::max(1, len(s) // 4)]], fontsize=9)
    ax.set_ylim(0, 700)
axs[0].set_ylabel("Sales (Rs thousand)")
fig.savefig("ch08v_lie_range.png", dpi=110)
print(f"Dec 2024 to Jan 2025: {350 / 620 - 1:+.1%}")
print(f"Jan 2024 to Oct 2024: {470 / 310 - 1:+.1%}")
print(f"Jan 2024 to Jun 2025: {455 / 310 - 1:+.1%}; Jan 2025 vs Jan 2024: {350 / 310 - 1:+.1%}")
print("saved")
