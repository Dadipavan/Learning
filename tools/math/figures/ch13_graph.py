import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

BLUE, ORANGE, TEAL, RED = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26"

def node(ax, xy, label, val, grad):
    ax.add_patch(Circle(xy, 0.42, fc="white", ec="#333", lw=1.6, zorder=3))
    ax.text(xy[0], xy[1], label, ha="center", va="center", fontsize=13, zorder=4)
    ax.text(xy[0], xy[1] + 0.68, f"value {val}", ha="center", color=BLUE, fontsize=10)
    ax.text(xy[0], xy[1] - 0.78, f"grad {grad}", ha="center", color=RED, fontsize=10)

def edge(ax, a, b, color="#555"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14, color=color, lw=1.4,
                                 shrinkA=17, shrinkB=17, zorder=2))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
ax = axes[0]
P = {"x": (0.8, 3.0), "y": (0.8, 1.0), "q": (3.4, 2.0), "z": (3.4, -0.4), "f": (6.0, 1.2)}
vals = {"x": -2, "y": 5, "q": 3, "z": -4, "f": -12}
grad = {"x": -4, "y": -4, "q": -4, "z": 3, "f": 1}
labs = {"x": "x", "y": "y", "q": "+", "z": "z", "f": "×"}
for a, b in [("x", "q"), ("y", "q"), ("q", "f"), ("z", "f")]:
    edge(ax, P[a], P[b])
for k in P:
    node(ax, P[k], labs[k], vals[k], grad[k])
ax.set_xlim(-0.3, 7); ax.set_ylim(-1.6, 4.0); ax.axis("off")
ax.set_title("f = (x + y) · z   at x=-2, y=5, z=-4", fontsize=11)

ax = axes[1]
P = {"x": (0.8, 2.4), "y": (0.8, 0.0), "a": (3.4, 2.4), "b": (3.4, 0.0), "c": (6.0, 1.2)}
vals = {"x": 2, "y": 3, "a": 6, "b": 5, "c": 30}
grad = {"x": 21, "y": 16, "a": 5, "b": 6, "c": 1}
labs = {"x": "x", "y": "y", "a": "×", "b": "+", "c": "×"}
for a, b in [("x", "a"), ("y", "a"), ("x", "b"), ("y", "b"), ("a", "c"), ("b", "c")]:
    edge(ax, P[a], P[b])
for k in P:
    node(ax, P[k], labs[k], vals[k], grad[k])
ax.set_xlim(-0.3, 7); ax.set_ylim(-1.6, 4.0); ax.axis("off")
ax.set_title("c = (x·y)(x + y), x and y fan out", fontsize=11)
fig.tight_layout()
fig.savefig("ch13_graph.png", dpi=110)
