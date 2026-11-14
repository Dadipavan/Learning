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

pos = {0: (0, 0), 1: (2, 1.2), 2: (2, -1.2), 3: (4, 1.2), 4: (4, -1.2), 5: (6, 0)}
E = [(0,1),(0,2),(1,3),(2,3),(2,4),(3,5),(4,5)]
fig, (ax, bx) = plt.subplots(1, 2, figsize=(9, 4.2), gridspec_kw={"width_ratios": [1.15, 1]})
setup(ax, (-0.6, 6.6), (-2, 2))
for a, b in E: edge(ax, pos[a], pos[b])
for k, p in pos.items(): node(ax, p, k)
ax.set_title("The graph: 6 nodes, 7 edges", fontsize=15)
bx.axis("off"); bx.set_xlim(0, 1); bx.set_ylim(0, 1)
bx.text(0.0, 0.97, "Adjacency list", fontsize=15, color=B, fontweight="bold", va="top")
adj = {0:[1,2],1:[0,3],2:[0,3,4],3:[1,2,5],4:[2,5],5:[3,4]}
for i, (k, v) in enumerate(adj.items()):
    bx.text(0.0, 0.85 - i*0.085, "%d: %s" % (k, v), family="monospace", fontsize=14, va="top")
bx.text(0.0, 0.33, "Edge list", fontsize=15, color=O, fontweight="bold", va="top")
bx.text(0.0, 0.24, "(0,1) (0,2) (1,3) (2,3)\n(2,4) (3,5) (4,5)", family="monospace", fontsize=13, va="top")
plt.tight_layout(); plt.savefig("dsa8_repr.png", dpi=110)
