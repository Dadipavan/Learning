from common import *
from matplotlib.patches import Rectangle
fig, ax = canvas(8, 4.4)
ax.set_xlim(0, 10); ax.set_ylim(0, 5.4)
for (x, y, w, h, c, t) in [(0.3, 0.3, 9.4, 4.4, BLUE, "@log  (outer): runs first on the way in, last on the way out"),
                           (1.2, 0.9, 7.6, 3.0, ORANGE, "@retry  (middle)"),
                           (2.1, 1.5, 5.8, 1.6, TEAL, "")]:
    ax.add_patch(Rectangle((x, y), w, h, fc=LIGHT[c], ec=c, lw=1.8))
ax.text(5, 4.4, "@log  (outer layer)", ha="center", fontsize=11, color=BLUE, fontweight="bold")
ax.text(5, 3.55, "@retry  (middle layer)", ha="center", fontsize=11, color=ORANGE, fontweight="bold")
ax.text(5, 2.3, "the original function", ha="center", fontsize=11, color=TEAL, fontweight="bold")
ax.text(0.3, 5.05, "Stacked decorators:  @log above @retry above def work()", fontsize=11, fontweight="bold")
arrow(ax, 0.0, 4.2, 0.6, 4.2, GREY); ax.text(0.0, 4.4, "call", fontsize=9)
save(fig, "ch07_decorator_onion.png")
