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

fig, (ax, bx) = plt.subplots(1, 2, figsize=(9, 4.2))
setup(ax, (0.3, 4.2), (-0.7, 4.0)); setup(bx, (0.3, 4.2), (-0.7, 4.0))
p1 = {0: (1.5, 3.2), 1: (1.5, 2.2), 2: (1.5, 1.2), 3: (1.5, 0.2), 4: (3.0, 2.2)}
for c, par in [(1,0),(2,1),(3,2),(4,0)]: edge(ax, p1[c], p1[par], r=0.3, directed=True, color=O)
for k, p in p1.items(): node(ax, p, k, r=0.3)
ax.set_title("Before: a tall chain", fontsize=15)
p2 = {0: (2.25, 3.2), 1: (0.9, 1.6), 2: (1.9, 1.6), 3: (2.9, 1.6), 4: (3.7, 1.6)}
for c in [1,2,3,4]: edge(bx, p2[c], p2[0], r=0.3, directed=True, color=T)
for k, p in p2.items(): node(bx, p, k, r=0.3)
bx.set_title("After find(3) with compression", fontsize=15)
plt.tight_layout(); plt.savefig("dsa8_uf.png", dpi=110)
