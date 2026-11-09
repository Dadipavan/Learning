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
arr = [1, 2, 1, 3, 5, 6, 4]
ax.plot(range(7), arr, color="#999999", lw=2, zorder=1)
ax.scatter(range(7), arr, s=160, color=BLUE, zorder=2)
for i, v in enumerate(arr):
    ax.text(i, v + 0.35, str(v), ha="center", fontsize=14)
steps = [(3, 4, "step 1: mid=3, 3 < 5, climb right", ORANGE, 0.0),
         (5, 6, "step 2: mid=5, 6 > 4, peak is at 5 or left", RED, 0.0),
         (4, 5, "step 3: mid=4, 5 < 6, climb right", TEAL, 0.0)]
ax.scatter([5], [6], s=420, facecolors="none", edgecolors=PURPLE, linewidths=3, zorder=3)
ax.text(5.1, 7.15, "peak", ha="center", fontsize=14, color=PURPLE, fontweight="bold")
ax.annotate("", xy=(4, 5), xytext=(3, 3), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=3))
ax.annotate("", xy=(5, 6), xytext=(4, 5), arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=3))
ax.text(0.0, 6.9, "step 1: mid=3, a[3]=3 < a[4]=5: go right\nstep 2: mid=5, a[5]=6 > a[6]=4: keep mid, go left\nstep 3: mid=4, a[4]=5 < a[5]=6: go right", fontsize=11.5, va="top")
ax.set_xticks(range(7)); ax.set_xlabel("index", fontsize=14); ax.set_ylabel("value", fontsize=14)
ax.set_ylim(0, 8); ax.set_xlim(-0.5, 6.5)
ax.set_title("Peak finding: always step toward the bigger neighbour", fontsize=14)
save(fig, "dsa4_peak.png")
