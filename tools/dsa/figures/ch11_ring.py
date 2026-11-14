import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *
import math
import matplotlib.patches as mp

fig, ax = plt.subplots(figsize=(8, 4.2))
ax.set_xlim(-2.9, 2.9)
ax.set_ylim(-1.6, 1.6)
ax.axis("off")
ax.set_aspect("equal")
t = [i / 100 * 2 * math.pi for i in range(101)]
ax.plot([math.cos(a) for a in t], [math.sin(a) for a in t], color=GREY, lw=2)


def P(deg, r=1.0):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))


for name, d, c, ls in (("A", 30, BLUE, "-"), ("B", 150, ORANGE, "-"), ("C", 270, TEAL, "-"), ("D", 215, PURPLE, "--")):
    x, y = P(d)
    ax.add_patch(mp.Circle((x, y), 0.15, fc="white", ec=c, lw=3, ls=ls, zorder=4))
    ax.text(x, y, name, ha="center", va="center", fontsize=13, color=c, weight="bold", zorder=5)
for name, d in (("k1", 100), ("k2", 190), ("k3", 330)):
    x, y = P(d)
    ax.scatter([x], [y], s=90, color=RED, zorder=4)
    x2, y2 = P(d, 1.3)
    ax.text(x2, y2, name, ha="center", va="center", fontsize=13, color=RED)
ax.text(1.35, 0.1, "a key belongs to the\nnext node met going\nanticlockwise (the\nlast wraps to the first)", fontsize=11, color=GREY, va="center")
ax.text(-2.85, -1.0, "add D: only k2 moves\n(from C to D)", fontsize=13, color=PURPLE)
ax.text(0, 0, "hash ring", fontsize=14, color=BLUE, ha="center", va="center", weight="bold")
save(fig, "dsa11_ring.png")
