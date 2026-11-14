import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

B, O, T, R = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26"
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
nodes = {"x": (1, 4.4), "y": (1, 1.4), "a = x*y": (4.2, 1.9), "b = x^2": (4.2, 4.6), "z": (8, 3.2)}
fwd = {"x": "2", "y": "-3", "a = x*y": "-6", "b = x^2": "4", "z": "-2"}
bwd = {"x": "1", "y": "2", "a = x*y": "1", "b = x^2": "1", "z": "1"}
for k, (x, y) in nodes.items():
    ax.add_patch(Circle((x, y), 0.62, fc="white", ec="#333333", lw=2))
    ax.text(x, y + 0.12, k, ha="center", va="center", fontsize=11)
    ax.text(x, y - 0.3, fwd[k], ha="center", va="center", fontsize=13, color=B, fontweight="bold")
    ax.text(x, y + 0.95, "grad " + bwd[k], ha="center", va="center", fontsize=12, color=O, fontweight="bold")
def arr(a, b, col="#444444", rad=0.0):
    (x1, y1), (x2, y2) = nodes[a], nodes[b]
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16, color=col, lw=2,
                                 shrinkA=26, shrinkB=26, connectionstyle=f"arc3,rad={rad}"))
arr("x", "a = x*y"); arr("y", "a = x*y"); arr("x", "b = x^2", rad=-0.0)
arr("a = x*y", "z"); arr("b = x^2", "z")
ax.text(2.3, 3.0, "via a: 1 x y = -3", color=R, fontsize=11, ha="center")
ax.text(2.6, 5.45, "via b: 1 x 2x = 4", color=R, fontsize=11, ha="center")
ax.text(5, 0.3, "x total: -3 + 4 = 1      y total: 1 * x = 2", ha="center", fontsize=12, color=T, fontweight="bold")
fig.tight_layout()
fig.savefig("lib21_autograd_graph.png", dpi=110)
