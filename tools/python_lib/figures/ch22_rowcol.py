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
cols = ["id", "region", "amount", "ts"]
for ax, title in zip(axs, ["Row store (CSV, sqlite3)", "Column store (Parquet)"]):
    ax.set_xlim(0, 4); ax.set_ylim(-0.9, 5.2); ax.axis("off"); ax.set_title(title)
for r in range(4):
    for c in range(4):
        hot = c == 2
        axs[0].add_patch(Rectangle((c, 3.6 - r), 1, 0.9, fc="#f3c9b8" if hot else "#dfe6fb", ec="white", lw=2))
        axs[0].text(c + .5, 4.05 - r, "", ha="center", va="center", fontsize=11)
        axs[1].add_patch(Rectangle((c, 3.6 - r), 1, 0.9, fc="#cfe4df" if not hot else "#f3c9b8", ec="white", lw=2))
for c in range(4):
    axs[1].text(c + .5, 4.7, cols[c], ha="center", fontsize=12, color=OR if c == 2 else "#222")
    axs[0].text(c + .5, 4.7, cols[c], ha="center", fontsize=12, color=OR if c == 2 else "#222")
axs[0].text(2, -0.35, "SUM(amount) must read\nevery byte of every row", ha="center", fontsize=12, color=RE)
axs[1].text(2, -0.35, "SUM(amount) reads one\ncolumn: about 1/4 of bytes", ha="center", fontsize=12, color=TE)
fig.tight_layout(); fig.savefig("lib22_rowcol.png", dpi=110)
