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

fig, ax = plt.subplots(figsize=(8, 4.2)); ax.set_xlim(0, 16); ax.set_ylim(0, 8); ax.axis("off")
box(ax, 0.2, 3.4, 2.6, 1.2, "sales/", "#dfe6fb", BL, 13)
yrs = [("year=2024", "#e6e6e6", "#888888"), ("year=2025", "#cfe4df", TE)]
for i, (t, fc, ec) in enumerate(yrs):
    y = 5.0 - i * 3.6
    box(ax, 4.2, y, 3.0, 1.1, t, fc, ec, 12); arrow(ax, 2.8, 4.0, 4.2, y + .55)
    for j, r in enumerate(["region=EU", "region=US"]):
        yy = y + 1.1 - j * 1.3 - 0.35 if False else y + 0.9 - j * 1.4 + 0.2
        hit = (i == 1 and j == 0); box(ax, 8.6, yy - 0.1, 2.6, 0.9, r, "#cfe4df" if hit else "#e6e6e6", TE if hit else "#888888", 11); arrow(ax, 7.2, y + .55, 8.6, yy + .35)
        ax.text(11.4, yy + .35, "part-0.parquet", va="center", fontsize=10, color="#333")
ax.text(15.8, 7.6, "Query: year = 2025 AND region = 'EU'", ha="right", fontsize=12, color=PU)
ax.text(0.2, 0.4, "green = the only file opened", ha="left", fontsize=11, color=TE)
ax.text(15.8, 0.4, "grey = skipped without reading", ha="right", fontsize=11, color="#555")
fig.tight_layout(); fig.savefig("lib22_layout.png", dpi=110)
