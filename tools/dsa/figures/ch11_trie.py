import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *
import matplotlib.patches as mp

fig, ax = canvas(16, 8.4)
txt(ax, 8, 7.9, "Autocomplete: walk the prefix, then take the top 2", BLUE, 16, weight="bold")
pos = {"root": (3, 6.8), "c": (3, 5.4), "a": (3, 4.0), "r": (1.8, 2.7), "t": (4.6, 2.7), "d": (0.9, 1.4), "e": (2.7, 1.4)}
edges = [("root", "c"), ("c", "a"), ("a", "r"), ("a", "t"), ("r", "d"), ("r", "e")]
for u, v in edges:
    ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=GREY, lw=2, zorder=1)
ends = {"r": "car 5", "t": "cat 2", "d": "card 3", "e": "care 7"}
for k, (x, y) in pos.items():
    col = TEAL if k in ends else BLUE
    ax.add_patch(mp.Circle((x, y), 0.5, fc="white", ec=col, lw=3, zorder=3))
    txt(ax, x, y, k if k != "root" else "root", col, 15 if k != "root" else 10, weight="bold")
for k, s in ends.items():
    x, y = pos[k]
    if k in ("d", "e"):
        txt(ax, x, y - 0.85, s, TEAL, 12)
    else:
        txt(ax, x + 1.25, y, s, TEAL, 12)
ax.add_patch(Rectangle((0.0, 0.1), 6.9, 4.8, fc="none", ec=ORANGE, lw=2, ls="--", zorder=2))
txt(ax, 11.4, 6.0, "type 'ca'", ORANGE, 15, weight="bold")
txt(ax, 11.4, 4.8, "1. walk root, c, a", GREY, 13)
txt(ax, 11.4, 3.9, "2. collect words in the\ndashed subtree", GREY, 13)
txt(ax, 11.4, 2.7, "3. a heap keeps the best 2", GREY, 13)
txt(ax, 11.4, 1.5, "answer: care (7), car (5)", RED, 14, weight="bold")
save(fig, "dsa11_trie.png")
