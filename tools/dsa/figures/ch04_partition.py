import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
LT = {"blue": "#d6defa", "orange": "#f3d9cc", "teal": "#cfe5e0", "red": "#f1cfcc", "purple": "#e0d4f7", "grey": "#e4e4ea", "white": "#ffffff"}
plt.rcParams.update({"font.size": 14})

def cells(ax, vals, x0=0.0, y=0.0, fc=None, fs=16, idx=True, w=1.0, h=0.8):
    for i, v in enumerate(vals):
        c = LT[fc[i]] if fc and fc[i] else LT["white"]
        ax.add_patch(Rectangle((x0 + i * w, y), w, h, fc=c, ec="#333333", lw=1.5))
        ax.text(x0 + i * w + w / 2, y + h / 2, str(v), ha="center", va="center", fontsize=fs, color="#111111")
        if idx:
            ax.text(x0 + i * w + w / 2, y - 0.08, str(i), ha="center", va="top", fontsize=11, color="#666666")

def below(ax, x, y, label, color, fs=13):
    ax.annotate(label, xy=(x, y - 0.3), xytext=(x, y - 0.95), ha="center", va="top", fontsize=fs, color=color,
                fontweight="bold", arrowprops=dict(arrowstyle="-|>", color=color, lw=2))

def above(ax, x, y, label, color, fs=13):
    ax.annotate(label, xy=(x, y + 0.85), xytext=(x, y + 1.35), ha="center", va="bottom", fontsize=fs, color=color,
                fontweight="bold", arrowprops=dict(arrowstyle="-|>", color=color, lw=2))

def save(fig, name):
    fig.savefig(name, dpi=110, bbox_inches="tight", facecolor="white")
fig, ax = plt.subplots(figsize=(8, 5.6))
P = 5
rows = [
 ([8,3,7,1,6,2,5], ["grey"]*6 + ["purple"], "start", None, 0),
 ([3,1,7,8,6,2,5], ["teal","teal","orange","orange","grey","grey","purple"], "after j=3", 1, 4),
 ([3,1,2,8,6,7,5], ["teal","teal","teal","orange","orange","orange","purple"], "loop done", 2, None),
 ([3,1,2,5,6,7,8], ["teal","teal","teal","purple","orange","orange","orange"], "pivot swapped in", None, None)]
for r, (arr, fc, lab, i, j) in enumerate(rows):
    y = (3 - r) * 2.1
    cells(ax, arr, x0=2.2, y=y, fc=fc, idx=False)
    ax.text(2.0, y + 0.4, lab, ha="right", va="center", fontsize=13, color=BLUE)
    if i is not None: below(ax, 2.2 + i + 0.5, y, "i", TEAL)
    if j is not None: above(ax, 2.2 + j + 0.5, y, "j", ORANGE)
ax.text(2.2, 8.45, "teal = at most 5   orange = more than 5   grey = unseen   purple = pivot 5", fontsize=11.5, va="bottom")
ax.set_xlim(0, 9.5); ax.set_ylim(-1.2, 9.3); ax.axis("off")
save(fig, "dsa4_partition.png")
