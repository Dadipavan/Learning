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
piles = [3, 6, 7, 11]
H = 8
sp = list(range(1, 13))
hrs = [sum(math.ceil(p / s) for p in piles) for s in sp]
fig, ax = plt.subplots(figsize=(8, 4.2))
cols = [RED if h > H else TEAL for h in hrs]
ax.bar(sp, hrs, color=cols, width=0.7)
for s, h in zip(sp, hrs):
    ax.text(s, h + 0.4, str(h), ha="center", fontsize=12)
ax.axhline(H, color=PURPLE, lw=2.5, ls="--")
ax.text(12.4, H + 0.6, "limit H = 8 hours", ha="right", fontsize=13, color=PURPLE)
ax.annotate("smallest good speed = 4", xy=(4, 8), xytext=(5.2, 17), fontsize=13, color=TEAL,
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2))
ax.set_xticks(sp); ax.set_xlabel("eating speed k (bananas per hour)", fontsize=14)
ax.set_ylabel("hours needed", fontsize=14)
ax.set_title("Piles 3, 6, 7, 11: red too slow, teal fast enough", fontsize=14)
save(fig, "dsa4_answer.png")
