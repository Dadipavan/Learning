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

pos = {0: (0, 0), 1: (2, 2), 2: (3, 0), 3: (5.8, 2), 4: (5.8, -1.8), 5: (2.6, -1.8)}
W = {(0,1):7,(0,2):9,(0,5):14,(1,2):10,(1,3):15,(2,3):11,(2,5):2,(3,4):6,(4,5):9}

mst = {(2,5),(3,4),(0,1),(0,2),(4,5)}
order = {(2,5):1,(3,4):2,(0,1):3,(0,2):4,(4,5):5}
fig, ax = plt.subplots(figsize=(8, 4.2))
setup(ax, (-0.7, 6.7), (-2.6, 2.7))
for (a, b), w in W.items():
    on = (a, b) in mst
    edge(ax, pos[a], pos[b], color=T if on else "#bbbbbb", lw=4.5 if on else 2, ls="-" if on else "--")
    m = ((pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2)
    ax.text(m[0], m[1], str(w), ha="center", va="center", fontsize=14, color=R if on else "#777777", fontweight="bold", zorder=5,
            bbox=dict(fc="white", ec="none", pad=1.5))
for k, p in pos.items(): node(ax, p, k)
ax.set_title("Minimum spanning tree: 5 edges, total weight 33", fontsize=15)
plt.tight_layout(); plt.savefig("dsa8_mst.png", dpi=110)
