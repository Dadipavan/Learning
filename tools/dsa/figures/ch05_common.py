import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
GREY = "#555555"
plt.rcParams.update({"font.size": 14, "font.family": "DejaVu Sans"})


def canvas(xmax=16, ymax=8.4, size=(8, 4.2)):
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text="", ec=BLUE, fc="white", fs=15, lw=2, tc="black"):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=2))
    if text != "":
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, zorder=3)


def arrow(ax, p, q, color=GREY, lw=2, rad=0.0, style="-|>", ms=16):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=ms, color=color,
                                 lw=lw, connectionstyle=f"arc3,rad={rad}", zorder=4))


def txt(ax, x, y, s, color="black", fs=14, ha="center", va="center", weight="normal"):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color, weight=weight, zorder=5)


def save(fig, name):
    fig.tight_layout(pad=0.4)
    fig.savefig(name, dpi=110)
