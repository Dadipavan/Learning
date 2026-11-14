import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
reasons = pd.Series({"Size or fit": 124, "Damaged in transit": 86, "Late delivery": 51,
                     "Wrong item": 33, "Changed mind": 21, "Other": 15}).sort_values(ascending=False)
cum = reasons.cumsum() / reasons.sum() * 100
print(pd.DataFrame({"returns": reasons, "cum_pct": cum.round(1)}).to_string())
fig, ax = plt.subplots()
ax.bar(reasons.index, reasons.values, color=[BLUE, BLUE] + [GREY] * 4)
ax.set_ylabel("Returns (count)")
ax.set_xticks(range(len(reasons)), reasons.index, rotation=20, ha="right")
ax2 = ax.twinx()
ax2.plot(range(len(reasons)), cum.values, color=ORANGE, marker="o", lw=2.5)
ax2.set_ylim(0, 105); ax2.set_ylabel("Cumulative share of returns (%)")
ax2.spines["right"].set_visible(True)
ax2.axhline(80, color=ORANGE, lw=1, ls="--")
ax2.text(5, 82, "80%", color=ORANGE, ha="right")
ax.set_title("Two reasons cause 64% of returns")
fig.tight_layout()
fig.savefig("ch08v_pareto.png", dpi=110)
print("saved")
