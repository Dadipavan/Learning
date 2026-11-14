"""Shared drawing helpers for Chapter 3 figures (arrays with pointer arrows)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
LIGHT = {BLUE: "#dbe3fb", ORANGE: "#f6e0d6", TEAL: "#d6eae6", RED: "#f3d6d4", PURPLE: "#e4d8f8"}


def new_fig(w=8, h=4.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.axis("off")
    ax.set_aspect("equal")
    return fig, ax


def draw_array(ax, vals, y=0.0, x0=0.0, fills=None, fs=17, idx=True, cell=1.0):
    """Draw boxes with values. fills maps index -> colour key from LIGHT."""
    fills = fills or {}
    for i, v in enumerate(vals):
        face = LIGHT.get(fills.get(i), "white")
        ax.add_patch(Rectangle((x0 + i * cell, y), cell, cell, fc=face, ec="#333333", lw=1.6))
        ax.text(x0 + i * cell + cell / 2, y + cell / 2, str(v), ha="center", va="center", fontsize=fs)
        if idx:
            ax.text(x0 + i * cell + cell / 2, y - 0.22, str(i), ha="center", va="top", fontsize=11, color="#666666")


def pointer(ax, i, y, text, color, x0=0.0, below=True, length=0.7, fs=15, cell=1.0):
    """Arrow pointing at box i from below (or above) with a label."""
    cx = x0 + i * cell + cell / 2
    if below:
        start, end = y - 0.45 - length, y - 0.45
        ax.annotate("", xy=(cx, end), xytext=(cx, start),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4))
        ax.text(cx, start - 0.1, text, ha="center", va="top", fontsize=fs, color=color, fontweight="bold")
    else:
        start, end = y + cell + 0.12 + length, y + cell + 0.12
        ax.annotate("", xy=(cx, end), xytext=(cx, start),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4))
        ax.text(cx, start + 0.1, text, ha="center", va="bottom", fontsize=fs, color=color, fontweight="bold")


def save(fig, name):
    fig.savefig(name, dpi=110, bbox_inches="tight", facecolor="white")
