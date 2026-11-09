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
iv = [(1,3),(2,6),(8,10),(15,18),(17,20)]
for k, (a, b) in enumerate(iv):
    y = 5 - k
    ax.barh(y, b - a, left=a, height=0.6, color=BLUE)
    ax.text(a - 0.3, y, "[%d,%d]" % (a, b), ha="right", va="center", fontsize=12)
merged = [(1,6),(8,10),(15,20)]
for a, b in merged:
    ax.barh(-0.3, b - a, left=a, height=0.7, color=TEAL)
    ax.text((a + b) / 2, -0.3, "[%d,%d]" % (a, b), ha="center", va="center", fontsize=11, color="white", fontweight="bold")
ax.axhline(0.6, color="#aaaaaa", lw=1)
ax.text(21, 3, "sorted by\nstart", fontsize=13, color=BLUE, va="center", ha="right")
ax.text(0.5, -0.3, "merged", fontsize=13, color=TEAL, va="center", ha="right")
ax.set_xlim(-2, 21.5); ax.set_ylim(-1.1, 5.8); ax.set_yticks([])
ax.set_xlabel("time", fontsize=14)
ax.set_title("Sort by start, then sweep: overlapping bars merge", fontsize=14)
save(fig, "dsa4_intervals.png")
