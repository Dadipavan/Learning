import sys, os
sys.path.insert(0, "/Users/c2487352/Personal/Career/final/tools/figs_de")
from common import *
import numpy as np
sizes = [3, 2, 5, 1, 4, 2, 6, 3, 2, 1, 4, 5, 3, 2, 800, 4]
fig, axs = plt.subplots(1, 3, figsize=(11, 3.8), gridspec_kw={"width_ratios": [1.3, 1, 1.3]})
ax = axs[0]
ax.bar(range(16), sizes, color=[RED if s > 256 else BLUE for s in sizes])
ax.set_title("1. Before: 16 shuffle partitions"); ax.set_xlabel("partition"); ax.set_ylabel("MB")
ax.annotate("800 MB\nskewed", (14, 800), (6, 600), arrowprops=dict(arrowstyle="->"), color=RED)
ax = axs[1]
groups = [sum(sizes[:14]), 800, 4]
ax.bar(["0-13\ncoalesced", "14\nskewed", "15"], [sum(sizes[:14]), 800, 4], color=[TEAL, RED, TEAL])
ax.set_title("2. Coalesce small ones"); ax.set_ylabel("MB")
ax = axs[2]
parts = [800/13]*13
ax.bar(range(13), parts, color=ORANGE)
ax.set_title("3. Split the skewed one (13 pieces)"); ax.set_xlabel("sub-task of partition 14"); ax.set_ylabel("MB")
ax.set_ylim(0, 100)
fig.tight_layout()
fig.savefig("de_aqe_steps.png", dpi=110, bbox_inches="tight")
