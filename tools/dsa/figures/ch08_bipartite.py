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
def ring(ax, n, colors, bad=None):
    setup(ax, (-1.6, 1.6), (-1.6, 1.6))
    pts = [(1.15 * np.cos(2 * np.pi * i / n + np.pi / 2), 1.15 * np.sin(2 * np.pi * i / n + np.pi / 2)) for i in range(n)]
    for i in range(n):
        j = (i + 1) % n
        edge(ax, pts[i], pts[j], r=0.0, color=R if bad == (i, j) else "#555555", lw=5 if bad == (i, j) else 2.5)
    for i in range(n): node(ax, pts[i], i, fc=colors[i], ec=colors[i], r=0.28, tc="white")
ring(ax, 6, [B, O, B, O, B, O]); ax.set_title("6-cycle: 2 colours work", fontsize=15)
ring(bx, 5, [B, O, B, O, B], bad=(4, 0)); bx.set_title("5-cycle: edge 4-0 clashes", fontsize=15)
plt.tight_layout(); plt.savefig("dsa8_bipartite.png", dpi=110)
