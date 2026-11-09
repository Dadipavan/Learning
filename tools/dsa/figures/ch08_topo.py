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

pos = {5: (0, 1.3), 4: (0, -1.3), 2: (2.4, 1.3), 0: (2.4, -1.3), 3: (4.8, 1.3), 1: (4.8, -0.2)}
E = [(5,2),(5,0),(4,0),(4,1),(2,3),(3,1)]
rnd = {4: 0, 5: 0, 0: 1, 2: 1, 3: 2, 1: 3}
col = [B, T, O, P]
fig, ax = plt.subplots(figsize=(8, 4.2))
setup(ax, (-0.8, 6.8), (-2.4, 2.4))
for a, b in E: edge(ax, pos[a], pos[b], directed=True)
for k, p in pos.items():
    node(ax, p, k, fc=col[rnd[k]], ec=col[rnd[k]], tc="white")
for i, t in enumerate(["round 0: indegree 0", "round 1", "round 2", "round 3"]):
    ax.text(6.0, 1.7 - i * 0.55, t, fontsize=13, color=col[i], fontweight="bold")
ax.set_title("Course DAG: arrow a -> b means a must come first", fontsize=15)
plt.tight_layout(); plt.savefig("dsa8_topo.png", dpi=110)
