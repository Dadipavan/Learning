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
    ax.annotate(label, xy=(x, y + 0.05), xytext=(x, y + 0.65), ha="center", va="bottom", fontsize=fs, color=color,
                fontweight="bold", arrowprops=dict(arrowstyle="-|>", color=color, lw=2))

def save(fig, name):
    fig.savefig(name, dpi=110, bbox_inches="tight", facecolor="white")
fig, ax = plt.subplots(figsize=(8, 4.4))
arr = [1,2,2,2,2,5,7]
x0 = 0.5
for k, (y, tgt) in enumerate([(2.6, 2), (0.2, 4)]):
    fc = ["orange" if v == tgt else "white" for v in arr]
    cells(ax, arr, x0=x0, y=y, fc=fc)
    if tgt == 2:
        for pos, lab, col, dy in [(1, "bisect_left(2) = 1", BLUE, 1.0), (5, "bisect_right(2) = 5", RED, 1.0)]:
            ax.plot([x0 + pos] * 2, [y - 0.15, y + 0.95], color=col, lw=3, ls="--")
            ax.text(x0 + pos, y + 1.05, lab, ha="center", va="bottom", fontsize=12.5, color=col, fontweight="bold")
        ax.text(x0 + 3.5, y - 0.75, "count of 2s = 5 - 1 = 4", ha="center", fontsize=13, color=TEAL)
    else:
        ax.plot([x0 + 5] * 2, [y - 0.15, y + 0.95], color=PURPLE, lw=3, ls="--")
        ax.text(x0 + 5, y + 1.05, "bisect_left(4) = bisect_right(4) = 5", ha="center", va="bottom", fontsize=12.5, color=PURPLE, fontweight="bold")
        ax.text(x0 + 3.5, y - 0.75, "4 is absent, 5 is where it would be inserted", ha="center", fontsize=13, color=TEAL)
ax.set_xlim(-0.3, 8.3); ax.set_ylim(-1.5, 4.9); ax.axis("off")
save(fig, "dsa4_bounds.png")
