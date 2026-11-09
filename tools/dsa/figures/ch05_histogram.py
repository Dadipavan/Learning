import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

h = [2, 1, 5, 6, 2, 3]
fig, ax = plt.subplots(figsize=(8, 4.4))
cols = [BLUE] * 6
ax.bar(range(6), h, width=1.0, color="#c9d3f5", edgecolor=BLUE, lw=2, zorder=2)
ax.add_patch(Rectangle((1.5, 0), 2, 5, fc="none", ec=RED, lw=4, zorder=4))
ax.text(2.5, 2.5, "area\n5 x 2 = 10", ha="center", va="center", color=RED, fontsize=15, weight="bold", zorder=6)
for i, v in enumerate(h):
    ax.text(i, v + 0.15, str(v), ha="center", fontsize=14, zorder=6)
ax.set_xticks(range(6)); ax.set_ylim(0, 7.2); ax.set_xlim(-0.6, 5.6)
ax.set_xlabel("index", fontsize=14); ax.set_ylabel("bar height", fontsize=14); ax.tick_params(labelsize=13)
ax.set_title("Largest rectangle: width spans bars at least as tall as 5", fontsize=13)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(pad=0.5); fig.savefig("dsa5_histogram.png", dpi=110)
