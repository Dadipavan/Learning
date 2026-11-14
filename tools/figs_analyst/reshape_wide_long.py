import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110); ax.set_xlim(0, 16); ax.set_ylim(0, 8.4); ax.axis("off")
def table(x0, y0, header, rows, colw, colors):
    for j, h in enumerate(header):
        ax.add_patch(Rectangle((x0 + sum(colw[:j]), y0), colw[j], 0.9, fc=colors[j], ec="white"))
        ax.text(x0 + sum(colw[:j]) + colw[j]/2, y0 + 0.45, h, ha="center", va="center", fontsize=10, fontweight="bold", color="white")
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            ax.add_patch(Rectangle((x0 + sum(colw[:j]), y0 - 0.9*(i+1)), colw[j], 0.9, fc="#f4f4f4", ec="white"))
            ax.text(x0 + sum(colw[:j]) + colw[j]/2, y0 - 0.9*(i+1) + 0.45, v, ha="center", va="center", fontsize=10)
ax.text(2.6, 7.9, "WIDE: one row per city", ha="center", fontsize=11, fontweight="bold")
table(0.2, 6.2, ["city", "jan", "feb"], [["Pune", "2000", "2900"], ["Delhi", "1500", "0"]], [1.4, 1.2, 1.2], ["#2b4fd6", "#b84a22", "#b84a22"])
ax.text(12.0, 7.9, "LONG: one row per city and month", ha="center", fontsize=11, fontweight="bold")
table(8.4, 6.2, ["city", "month", "revenue"], [["Pune", "jan", "2000"], ["Pune", "feb", "2900"], ["Delhi", "jan", "1500"], ["Delhi", "feb", "0"]], [1.4, 1.4, 1.6], ["#2b4fd6", "#b84a22", "#357a70"])
ax.add_patch(FancyArrowPatch((4.6, 5.3), (8.1, 4.8), arrowstyle="-|>", mutation_scale=18, color="#333"))
ax.text(6.3, 5.55, "melt / UNION ALL", ha="center", fontsize=10)
ax.add_patch(FancyArrowPatch((8.1, 3.6), (4.6, 4.1), arrowstyle="-|>", mutation_scale=18, color="#333"))
ax.text(6.3, 3.35, "pivot / SUM(CASE ...)", ha="center", fontsize=10)
ax.text(8.0, 0.6, "The month names move from column headers into a column of values, and back.\nWide is easier to read, long is easier to filter, group and plot.", ha="center", fontsize=10)
fig.tight_layout(); fig.savefig("reshape_wide_long.png")
