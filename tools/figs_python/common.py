import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#555555"
LIGHT = {BLUE: "#dbe3fb", ORANGE: "#f6ddd2", TEAL: "#d5e8e5", RED: "#f3d6d4", PURPLE: "#e4d9f8", GREY: "#e8e8e8"}
plt.rcParams.update({"font.size": 11, "font.family": "DejaVu Sans"})

def canvas(w=8, h=4.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_axis_off()
    return fig, ax

def box(ax, x, y, w, h, text, color=BLUE, fs=11, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=LIGHT[color], ec=color, lw=1.6))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color="#111")

def arrow(ax, x1, y1, x2, y2, color=GREY, text=None, fs=10, rad=0.0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.12, text, ha="center", fontsize=fs, color=color)

def save(fig, name):
    fig.savefig(name, dpi=110, bbox_inches="tight", facecolor="white")
