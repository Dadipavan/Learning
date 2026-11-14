# helper imported by the other ch05 figure scripts (same folder)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

def canvas(w=8, h=4.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    return fig, ax

def box(ax, x, y, w, h, text, color=BLUE, fs=8.5, fill=0.12, tc=None):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.5",
                       fc=color, ec=color, alpha=fill, lw=1.5)
    ax.add_patch(p)
    p2 = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.5",
                        fc="none", ec=color, lw=1.6)
    ax.add_patch(p2)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc or "#1a1a1a")

def arrow(ax, x1, y1, x2, y2, color="#444444", label=None, fs=7.5, dx=0, dy=1.5, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11,
                                 color=color, lw=1.4, linestyle=ls))
    if label:
        ax.text((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, label, fontsize=fs, color=color,
                ha="center", va="bottom")
