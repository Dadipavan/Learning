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
M = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
for r in range(3):
    fc = ["orange" if r * 4 + c == 5 else "white" for c in range(4)]
    cells(ax, M[r], x0=0.3, y=(2 - r) * 1.0 + 2.2, fc=fc, idx=False, w=0.9, h=0.8)
    ax.text(0.15, (2 - r) + 2.6, "row %d" % r, ha="right", va="center", fontsize=12, color=BLUE)
for c in range(4):
    ax.text(0.3 + c * 0.9 + 0.45, 5.1, "col %d" % c, ha="center", fontsize=12, color=BLUE)
flat = [v for row in M for v in row]
fc = ["orange" if i == 5 else "white" for i in range(12)]
cells(ax, flat, x0=0.3, y=0.0, fc=fc, fs=13, w=0.66, h=0.7)
ax.annotate("", xy=(0.3 + 5.5 * 0.66, 0.78), xytext=(4.0, 3.6),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.5))
ax.text(5.2, 3.7, "flat index 5\nrow = 5 // 4 = 1\ncol = 5 % 4 = 1\nvalue = 11", fontsize=14, color=ORANGE, va="center")
ax.text(0.3, -0.75, "read the grid row by row: it becomes one sorted list of 12", fontsize=13, color=TEAL)
ax.set_xlim(-0.8, 8.4); ax.set_ylim(-1.2, 5.5); ax.axis("off")
save(fig, "dsa4_matrix.png")
