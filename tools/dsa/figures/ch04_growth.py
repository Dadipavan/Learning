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
import math
fig, ax = plt.subplots(figsize=(8, 4.2))
ns = list(range(1, 51))
ax.plot(ns, [n * n for n in ns], color=RED, lw=3, label="n squared (bubble, selection, insertion)")
ax.plot(ns, [n * math.log2(n) for n in ns], color=TEAL, lw=3, label="n log2 n (merge, quick, Timsort)")
ax.plot(ns, ns, color=BLUE, lw=3, label="n (one pass)")
ax.annotate("2500", xy=(50, 2500), xytext=(40, 2300), fontsize=14, color=RED)
ax.annotate("282", xy=(50, 282), xytext=(41, 700), fontsize=14, color=TEAL, arrowprops=dict(arrowstyle="-|>", color=TEAL))
ax.set_xlabel("n (number of items)", fontsize=14); ax.set_ylabel("steps", fontsize=14)
ax.legend(fontsize=11, loc="upper left"); ax.grid(alpha=0.3)
ax.set_title("Work grows far faster for n squared", fontsize=14)
save(fig, "dsa4_growth.png")
