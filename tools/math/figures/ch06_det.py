import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
cases = [("A = [[2, 1], [0, 1.5]]", np.array([[2, 1], [0, 1.5]])),
         ("B = [[0, 1], [1, 0]] (swap)", np.array([[0, 1], [1, 0.0]])),
         ("C = [[2, 1], [4, 2]] (singular)", np.array([[2, 1], [4, 2.0]]))]
sq = np.array([[0, 1, 1, 0, 0], [0, 0, 1, 1, 0]], float)
fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.4))
for ax, (name, M) in zip(axes, cases):
    d = np.linalg.det(M)
    ax.fill(sq[0], sq[1], color="#999999", alpha=0.3, label="unit square (area 1)")
    im = M @ sq
    ax.fill(im[0], im[1], color=ORANGE, alpha=0.4)
    ax.plot(im[0], im[1], color=ORANGE, lw=2, label="image")
    ax.annotate("", xy=M[:, 0], xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=RED, lw=2.2))
    ax.annotate("", xy=M[:, 1], xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2.2))
    ax.set_xlim(-0.5, 4); ax.set_ylim(-0.5, 4); ax.set_aspect("equal"); ax.grid(alpha=0.3)
    ax.set_title(f"{name}\ndet = {d:.1f}", fontsize=10)
    ax.legend(loc="upper right", fontsize=8)
fig.tight_layout()
fig.savefig("ch06_det.png", dpi=110)
