import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#555555"
plt.rcParams.update({"font.size": 11, "axes.titlesize": 13, "axes.labelsize": 11, "font.family": "DejaVu Sans"})

def canvas(w=9, h=4.4, xlim=(0, 100), ylim=(0, 50)):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    return fig, ax

def box(ax, x, y, w, h, text, color=BLUE, fc=None, fs=10, tc="black", lw=1.6):
    fc = fc or (color + "22")
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2", ec=color, fc=fc, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc)

def arrow(ax, x1, y1, x2, y2, color=GREY, text=None, fs=9, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14, color=color, lw=1.6,
                                 connectionstyle=f"arc3,rad={rad}", linestyle=ls))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 1.6, text, ha="center", fontsize=fs, color=color)
