import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

t = [73, 74, 75, 71, 69, 72, 76, 73]
nxt = [1, 2, 6, 5, 5, 6, None, None]
fig, ax = plt.subplots(figsize=(8, 4.4))
ax.bar(range(8), t, color=BLUE, width=0.6, zorder=2)
for i, v in enumerate(t):
    ax.text(i, v - 1.3, str(v), ha="center", va="top", color="white", fontsize=13, zorder=5)
for i, j in enumerate(nxt):
    if j is None:
        ax.text(i, t[i] + 1.4, "none", ha="center", color=RED, fontsize=12)
    else:
        ax.annotate("", xy=(j, t[j] + 0.5), xytext=(i, t[i] + 0.5),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2, connectionstyle="arc3,rad=-0.4"))
ax.set_ylim(62, 82); ax.set_xticks(range(8)); ax.set_xlabel("index", fontsize=14)
ax.set_ylabel("temperature", fontsize=14); ax.tick_params(labelsize=13)
ax.set_title("Arrow = next strictly greater value to the right", fontsize=14)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(pad=0.5); fig.savefig("dsa5_next_greater.png", dpi=110)
