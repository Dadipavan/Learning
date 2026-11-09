import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

def row(ax, vals, y, fills, title):
    for i, v in enumerate(vals):
        ax.add_patch(Rectangle((i, y), 0.9, 0.9, fc=fills[i], ec="black", lw=1.5, alpha=0.9))
        ax.text(i + 0.45, y + 0.45, str(v), ha="center", va="center", fontsize=18, color="white", fontweight="bold")
        ax.text(i + 0.45, y - 0.3, str(i), ha="center", va="center", fontsize=12, color="#444")
    ax.text(-0.3, y + 0.45, title, ha="right", va="center", fontsize=13)

def ptr(ax, i, y, label, color, up=True):
    y0, y1 = (y - 1.25, y - 0.55) if up else (y + 2.2, y + 1.0)
    ax.annotate("", xy=(i + 0.45, y1), xytext=(i + 0.45, y0), arrowprops=dict(arrowstyle="-|>", color=color, lw=3))
    ax.text(i + 0.45, y0 - 0.1 if up else y0 + 0.1, label, ha="center", va="top" if up else "bottom", fontsize=15, color=color, fontweight="bold")

fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
vals = [1, 3, 12, 0, 0]
fills = [T, T, T, "#999999", "#999999"]
row(ax, [0, 1, 0, 3, 12], 2.6, [R, B, R, B, B], "start")
row(ax, vals, 0.2, fills, "after")
ptr(ax, 4, 2.6, "r", O, up=False)
ptr(ax, 3, 0.2, "w", P, up=True)
ax.text(2.4, 5.7, "Move zeros: r reads every cell, w = next write spot", ha="center", fontsize=14)
ax.text(2.4, -2.5, "at the end w = 3: cells from w onward become 0", ha="center", fontsize=13, color=P)
ax.set_xlim(-2.2, 5.3); ax.set_ylim(-2.9, 6.2)
ax.axis("off")
plt.tight_layout(); plt.savefig("dsa2_array_pointers.png"); 
