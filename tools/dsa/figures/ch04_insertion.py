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
fig, ax = plt.subplots(figsize=(8, 4.6))
rows = [([5,2,4,6,1,3], 1, None), ([2,5,4,6,1,3], 2, 0), ([2,4,5,6,1,3], 3, 1),
        ([2,4,5,6,1,3], 4, 3), ([1,2,4,5,6,3], 5, 0), ([1,2,3,4,5,6], 6, 2)]
labels = ["start", "key 2", "key 4", "key 6", "key 1", "key 3"]
for r, (arr, k, ins) in enumerate(rows):
    y = (5 - r) * 1.05
    fc = ["teal" if i < k else "grey" for i in range(6)]
    if ins is not None: fc[ins] = "orange"
    cells(ax, arr, x0=1.8, y=y, fc=fc, idx=False, h=0.8, fs=15)
    ax.text(1.6, y + 0.4, labels[r], ha="right", va="center", fontsize=13, color=BLUE)
ax.set_xlim(0, 8.2); ax.set_ylim(-0.3, 6.2); ax.axis("off")
ax.set_title("Insertion sort: teal = sorted prefix, orange = key just placed", fontsize=14)
save(fig, "dsa4_insertion.png")
