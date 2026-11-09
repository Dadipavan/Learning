import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch02common import *
import numpy as np
cities = ["Pune", "Mumbai", "Delhi"]; cats = ["Fashion", "Electronics", "Grocery"]
g = np.zeros((3, 3))
for r in ROWS:
    if r[6] == "Delivered": g[cities.index(r[2]), cats.index(r[3])] += r[4]*r[5]
fig, ax = newfig()
im = ax.imshow(g, cmap="Blues", vmin=0, vmax=3000)
for i in range(3):
    for j in range(3):
        ax.text(j, i, "%d" % g[i, j], ha="center", va="center", fontsize=12, color="white" if g[i, j] > 1800 else "#222")
ax.set_xticks(range(3)); ax.set_xticklabels(cats, fontsize=10); ax.set_yticks(range(3)); ax.set_yticklabels(cities, fontsize=10)
for j in range(3): ax.text(j, 2.75, "col: %d" % g[:, j].sum(), ha="center", fontsize=9, color=BLUE)
for i in range(3): ax.text(2.58, i, "row: %d" % g[i].sum(), va="center", fontsize=9, color=BLUE)
ax.set_xlim(-0.5, 3.4); ax.set_ylim(3.0, -0.5)
ax.set_title("=SUMIFS(Amount, City, row label, Category, column label, Status, \"Delivered\")\ngrand total = %d" % g.sum(), fontsize=10)
fig.tight_layout(); fig.savefig("ch02d_sumifs_grid.png")
