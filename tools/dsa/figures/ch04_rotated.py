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
fig, ax = plt.subplots(figsize=(8, 4.2))
arr = [4,5,6,7,0,1,2]
cols = [BLUE if i < 4 else ORANGE for i in range(7)]
ax.bar(range(7), arr, color=cols, width=0.7)
for i, v in enumerate(arr):
    ax.text(i, v + 0.15, str(v), ha="center", fontsize=15)
ax.set_xticks(range(7)); ax.set_xlabel("index", fontsize=14); ax.set_ylabel("value", fontsize=14)
ax.annotate("the drop:\nsmallest value\nsits here", xy=(4, 0.45), xytext=(4.15, 4.9), fontsize=13, color=RED,
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.text(1.5, 8.0, "sorted run 1", ha="center", fontsize=14, color=BLUE)
ax.text(5.3, 3.4, "sorted run 2", ha="center", fontsize=14, color=ORANGE)
ax.set_ylim(0, 9)
ax.set_title("Rotated array [4,5,6,7,0,1,2]: two sorted runs", fontsize=14)
save(fig, "dsa4_rotated.png")
