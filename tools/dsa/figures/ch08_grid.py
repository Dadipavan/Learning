import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 15})
def node(ax, xy, label, fc="white", ec=B, r=0.32, fs=17, tc="black"):
    ax.add_patch(Circle(xy, r, fc=fc, ec=ec, lw=2.5, zorder=3))
    ax.text(xy[0], xy[1], str(label), ha="center", va="center", fontsize=fs, color=tc, zorder=4, fontweight="bold")
def edge(ax, a, b, r=0.32, color="#555555", lw=2.5, directed=False, ls="-", rad=0.0):
    a = np.array(a, float); b = np.array(b, float); u = (b - a) / np.hypot(*(b - a))
    if directed:
        ax.annotate("", xy=b - u * r, xytext=a + u * r, zorder=2,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=24, connectionstyle="arc3,rad=%s" % rad))
    else:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, zorder=1, ls=ls)
def setup(ax, xl, yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal"); ax.axis("off")

g = ["11000", "11000", "00100", "00011", "00011"]
lab = {}
cols = {1: B, 2: O, 3: T}
cells = {1: [(0,0),(0,1),(1,0),(1,1)], 2: [(2,2)], 3: [(3,3),(3,4),(4,3),(4,4)]}
for k, v in cells.items():
    for c in v: lab[c] = k
fig, ax = plt.subplots(figsize=(8, 4.2))
for r in range(5):
    for c in range(5):
        k = lab.get((r, c))
        ax.add_patch(Rectangle((c, 4 - r), 1, 1, fc=cols[k] if k else "#eeeeee", ec="white", lw=3))
        ax.text(c + 0.5, 4 - r + 0.5, g[r][c], ha="center", va="center", fontsize=20, color="white" if k else "#999999", fontweight="bold")
    ax.text(-0.15, 4 - r + 0.5, "r%d" % r, ha="right", va="center", fontsize=13)
for c in range(5): ax.text(c + 0.5, 5.15, "c%d" % c, ha="center", fontsize=13)
ax.text(5.5, 3.0, "Island 1\n4 cells", fontsize=15, color=B, fontweight="bold", va="center")
ax.text(5.5, 2.0, "Island 2\n1 cell", fontsize=15, color=O, fontweight="bold", va="center")
ax.text(5.5, 0.9, "Island 3\n4 cells", fontsize=15, color=T, fontweight="bold", va="center")
ax.set_xlim(-0.8, 7.2); ax.set_ylim(-0.2, 5.6); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Grid islands: each colour is one DFS flood", fontsize=15)
plt.tight_layout(); plt.savefig("dsa8_grid.png", dpi=110)
