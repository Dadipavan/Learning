import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
pos = {}
for i in range(3):
    pos[i] = (1.5 + i * 2.2, 4.2)
cx, cy, R = 10.2, 4.2, 2.9
cyc = [3, 4, 5, 6, 7]
for k, n in enumerate(cyc):
    ang = math.pi + k * 2 * math.pi / 5
    pos[n] = (cx + R * math.cos(ang) + 0.0, cy - R * math.sin(ang))
# edges
for a in range(7):
    arrow(ax, pos[a], pos[a + 1], GREY, ms=14)
arrow(ax, pos[7], pos[3], GREY, rad=0.0, ms=14)
for n, (x, y) in pos.items():
    ax.add_patch(plt.Circle((x, y), 0.55, fc="white", ec=BLUE, lw=2, zorder=3))
    txt(ax, x, y, str(n), "black", 15)
x, y = pos[5]
ax.add_patch(plt.Circle((x, y), 0.8, fc="none", ec=RED, lw=3, zorder=4))
txt(ax, x, y + 1.35, "they meet here", RED, 13)
txt(ax, 3.7, 6.3, "tail", GREY, 13)
txt(ax, 3.7, 1.7, "slow: 1 step, fast: 2 steps", ORANGE, 13)
txt(ax, 10.2, 4.2, "cycle", TEAL, 15, weight="bold")
txt(ax, 6.2, 5.6, "entry", PURPLE, 13)
save(fig, "dsa5_floyd.png")
