import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np
BL, OR, TE, RE, PU = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 13, "axes.titlesize": 15})
def box(ax, x, y, w, h, text, fc="#ffffff", ec=BL, fs=12, tc="#111111", lw=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc)
def arrow(ax, x1, y1, x2, y2, c="#333333", lw=2, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=18, color=c, lw=lw))

fig, axs = plt.subplots(1, 2, figsize=(8, 4.2))
for ax in axs: ax.set_xlim(0, 5); ax.set_ylim(0, 6); ax.axis("off")
axs[0].set_title("Plan as you wrote it")
axs[1].set_title("Plan after optimizing")
for i, t in enumerate(["scan all 12 columns", "filter year == 2025", "select 3 columns", "group_by + sum"]):
    box(axs[0], 0.4, 4.6 - i * 1.4, 4.2, 0.95, t, "#f3dfd6", OR, 11)
    if i < 3: arrow(axs[0], 2.5, 4.6 - i * 1.4, 2.5, 4.6 - i * 1.4 - 0.45)
for i, t in enumerate(["scan 3 columns only,\nskip row groups\nwith year != 2025", "group_by + sum"]):
    box(axs[1], 0.4, 4.2 - i * 2.4, 4.2, 1.5, t, "#cfe4df", TE, 11)
arrow(axs[1], 2.5, 4.2, 2.5, 3.2)
axs[1].text(2.5, 0.4, "projection + predicate pushdown", ha="center", fontsize=12, color=PU)
fig.tight_layout(); fig.savefig("lib22_lazy.png", dpi=110)
