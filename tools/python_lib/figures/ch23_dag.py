import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
def box(x, y, t, c):
    ax.add_patch(FancyBboxPatch((x, y), 2.0, 1.0, boxstyle="round,pad=0.05", fc="white", ec=c, lw=2.5))
    ax.text(x + 1.0, y + 0.5, t, ha="center", va="center", fontsize=13)
def arr(a, b): ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", lw=2))
box(0.2, 2.5, "extract", B); box(3.0, 2.5, "validate", O); box(5.8, 3.9, "features", T); box(5.8, 1.1, "baseline", T)
box(8.6, 2.5, "evaluate", P); box(8.6, 0.2, "report", R)
arr((2.25, 3.0), (2.95, 3.0)); arr((5.05, 3.2), (5.75, 4.2)); arr((5.05, 2.8), (5.75, 1.8))
arr((7.85, 4.2), (8.65, 3.3)); arr((7.85, 1.6), (8.65, 2.7)); arr((9.6, 2.45), (9.6, 1.25))
ax.text(6.0, 5.6, "A DAG: arrows say who must finish first, no loops", ha="center", fontsize=13)
fig.tight_layout(); fig.savefig("lib23_dag.png")
