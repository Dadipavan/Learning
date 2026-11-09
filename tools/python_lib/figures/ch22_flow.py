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

fig, ax = plt.subplots(figsize=(8, 4.2)); ax.set_xlim(0, 16); ax.set_ylim(0, 8.4); ax.axis("off")
box(ax, 0.2, 6.6, 3.8, 1.4, "Fits in RAM after\ndtype fixes?", "#dfe6fb", BL, 11)
box(ax, 5.2, 6.6, 3.0, 1.4, "pandas\n(plus chunks)", "#cfe4df", TE, 12)
box(ax, 0.2, 4.2, 3.8, 1.4, "Fits on one\nmachine's disk?", "#dfe6fb", BL, 11)
box(ax, 5.2, 4.2, 3.0, 1.4, "SQL or code?", "#dfe6fb", BL, 12)
box(ax, 10.2, 5.3, 3.0, 1.2, "DuckDB", "#cfe4df", TE, 13)
box(ax, 10.2, 3.3, 3.0, 1.2, "Polars (lazy)", "#cfe4df", TE, 13)
box(ax, 0.2, 1.4, 3.8, 1.4, "Spark platform\nalready in place?", "#dfe6fb", BL, 11)
box(ax, 5.2, 2.0, 3.0, 1.1, "PySpark", "#f3dfd6", OR, 13)
box(ax, 5.2, 0.3, 3.0, 1.1, "Dask", "#f3dfd6", OR, 13)
for (x1,y1,x2,y2,t) in [(4.0,7.3,5.2,7.3,"yes"),(2.1,6.6,2.1,5.6,"no"),(4.0,4.9,5.2,4.9,"yes"),(2.1,4.2,2.1,2.8,"no"),(8.2,5.2,10.2,5.9,"SQL"),(8.2,4.6,10.2,3.9,"code"),(4.0,2.3,5.2,2.55,"yes"),(4.0,1.7,5.2,0.9,"no")]:
    arrow(ax,x1,y1,x2,y2); ax.text((x1+x2)/2-0.1,(y1+y2)/2+0.3,t,fontsize=11,color=RE)
ax.text(9.2, 1.8, "Rule: use the smallest tool\nthat finishes in time.\nEvery step right adds cost.", fontsize=12, color=PU)
fig.tight_layout(); fig.savefig("lib22_flow.png", dpi=110)
