import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch02common import *
import math
ns = [10, 100, 1000, 10000, 100000, 1000000]
lin = [n/2 for n in ns]; binr = [math.ceil(math.log2(n+1)) for n in ns]
fig, ax = newfig()
ax.loglog(ns, lin, "-o", color=ORANGE, lw=2, label="exact match, unsorted (scan, average n/2 looks)")
ax.loglog(ns, binr, "-o", color=TEAL, lw=2, label="binary search on sorted keys (at most log2(n+1) looks)")
for n, l, b in zip(ns, lin, binr):
    ax.text(n, l*1.5, "%g" % l, fontsize=8, ha="center", color=ORANGE)
    ax.text(n, b/1.7, "%d" % b, fontsize=8, ha="center", color=TEAL)
ax.set_xlabel("rows in the lookup table (n)", fontsize=11); ax.set_ylabel("cells examined per lookup", fontsize=11)
ax.set_title("Why 30,000 lookups into a 5,000-row table can be slow", fontsize=11)
ax.legend(fontsize=8.5, frameon=False, loc="upper left"); clean(ax)
fig.tight_layout(); fig.savefig("ch02d_search_cost.png")
