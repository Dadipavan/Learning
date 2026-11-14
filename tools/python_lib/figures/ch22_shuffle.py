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

fig, ax = plt.subplots(figsize=(8, 4.2)); ax.set_xlim(0, 12); ax.set_ylim(-0.5, 7); ax.axis("off")
cs = [BL, OR, TE]
for i in range(3):
    y = 5.0 - i * 2.2
    box(ax, 0.2, y, 2.6, 1.2, f"input part {i+1}\nA B C A B A", "#dfe6fb", BL, 10)
    box(ax, 4.6, y, 2.0, 1.2, "local\npartial sums", "#f3dfd6", OR, 10)
    box(ax, 9.4, y, 2.4, 1.2, ["keys A", "keys B", "keys C"][i] + "\nfinal sum", "#cfe4df", TE, 10)
    arrow(ax, 2.8, y + .6, 4.6, y + .6)
    for j in range(3):
        arrow(ax, 6.6, y + .6, 9.4, 5.6 - j * 2.2, c=cs[j], lw=1.4)
ax.text(8.0, 6.7, "shuffle: network + disk", ha="center", color=RE, fontsize=13)
ax.text(1.5, 0.0, "map side", ha="center", fontsize=12); ax.text(5.6, 0.0, "combine", ha="center", fontsize=12); ax.text(10.6, 0.0, "reduce side", ha="center", fontsize=12)
fig.tight_layout(); fig.savefig("lib22_shuffle.png", dpi=110)
