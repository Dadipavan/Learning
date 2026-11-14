import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 15})

def cells(ax, vals, x0=0, y=0, w=1.0, h=0.9, fc="white", ec="#333333", fs=17, colors=None):
    for i, v in enumerate(vals):
        c = colors[i] if colors and colors[i] else fc
        ax.add_patch(Rectangle((x0 + i * w, y), w, h, fc=c, ec=ec, lw=2))
        ax.text(x0 + i * w + w / 2, y + h / 2, str(v), ha="center", va="center", fontsize=fs, fontweight="bold")
        ax.text(x0 + i * w + w / 2, y - 0.25, str(i), ha="center", va="center", fontsize=12, color="#666666")

def arrow(ax, x, y_from, y_to, label, color):
    ax.annotate("", xy=(x, y_to), xytext=(x, y_from),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=3, mutation_scale=24))
    ax.text(x, y_from + (0.18 if y_from > y_to else -0.18), label, ha="center",
            va="bottom" if y_from > y_to else "top", fontsize=15, color=color, fontweight="bold")

def node(ax, xy, label, fc="white", ec=B, r=0.32, fs=16, tc="black"):
    ax.add_patch(Circle(xy, r, fc=fc, ec=ec, lw=2.5, zorder=3))
    ax.text(xy[0], xy[1], str(label), ha="center", va="center", fontsize=fs, color=tc, zorder=4, fontweight="bold")

def line(ax, a, b, r=0.32, color="#555555", lw=2.5):
    import math
    d = math.hypot(b[0] - a[0], b[1] - a[1]); ux, uy = (b[0] - a[0]) / d, (b[1] - a[1]) / d
    ax.plot([a[0] + ux * r, b[0] - ux * r], [a[1] + uy * r, b[1] - uy * r], color=color, lw=lw, zorder=1)
