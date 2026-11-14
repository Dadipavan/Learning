import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *
import matplotlib.patches as mp

fig, ax = canvas(16, 8.4)
txt(ax, 8, 7.9, "Merge accounts: emails are nodes, accounts are edges", BLUE, 16, weight="bold")
pos = {"a@x": (2.5, 4.4), "b@x": (6.0, 4.4), "c@x": (9.5, 4.4), "d@x": (13.5, 4.4)}
for u, v, col, lab in (("a@x", "b@x", BLUE, "account 1"), ("b@x", "c@x", ORANGE, "account 2")):
    ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=col, lw=4, zorder=1)
    txt(ax, (pos[u][0] + pos[v][0]) / 2, 5.7, lab, col, 13)
for k, (x, y) in pos.items():
    col = BLUE if k != "d@x" else TEAL
    ax.add_patch(mp.Circle((x, y), 0.8, fc="white", ec=col, lw=3, zorder=3))
    txt(ax, x, y, k, col, 14, weight="bold")
txt(ax, 13.5, 5.7, "account 3", TEAL, 13)
ax.add_patch(Rectangle((0.8, 3.0), 10.2, 3.2, fc="none", ec=PURPLE, lw=2, ls="--"))
txt(ax, 6.0, 2.3, "one component: a, b, c", PURPLE, 14)
txt(ax, 13.5, 2.3, "alone", TEAL, 14)
txt(ax, 8, 0.8, "union(a, b) and union(b, c) give a, b, c the same root", GREY, 13)
save(fig, "dsa11_accounts.png")
