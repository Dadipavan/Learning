import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch02common import *
fig, ax = newfig()
amts = [r[4]*r[5] for r in ROWS]; ids = [r[0] for r in ROWS]
def band(v): return "Big" if v >= 1000 else ("Medium" if v >= 500 else "Small")
col = {"Small": ORANGE, "Medium": TEAL, "Big": BLUE}
for lo, hi, n in [(0, 500, "Small"), (500, 1000, "Medium"), (1000, 2700, "Big")]:
    ax.axvspan(lo, hi, color=LIGHT[col[n]], alpha=0.9)
    ax.text((lo+min(hi, 2700))/2, 8.6, n, ha="center", fontsize=11, color=col[n], fontweight="bold")
    ax.text((lo+min(hi, 2700))/2, 8.1, "starts at %d" % lo, ha="center", fontsize=9, color="#333")
for i, (a, o) in enumerate(sorted(zip(amts, ids))):
    ax.plot(a, i+0.5, "o", color=col[band(a)], ms=9)
    ax.text(a+40, i+0.5, "%d  (%d)" % (a, o), va="center", fontsize=9)
ax.set_xlim(0, 2700); ax.set_ylim(0, 9.1); ax.set_yticks([])
ax.set_xlabel("Amount (Rs)", fontsize=11)
ax.set_title("Approximate match: each amount lands in the band whose start is the\nlargest start that is not above it", fontsize=10)
ax.text(1900, 0.4, "Note: 1000 is Big, because\nthe band start 1000 is exact", fontsize=9, color="#333")
clean(ax); ax.spines["left"].set_visible(False)
fig.tight_layout(); fig.savefig("ch02d_lookup_bands.png")
