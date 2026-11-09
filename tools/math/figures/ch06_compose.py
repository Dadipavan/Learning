import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
R = np.array([[0, -1], [1, 0.0]])      # rotate 90 degrees
S = np.array([[1, 1], [0, 1.0]])       # shear
F = np.array([[0, 0, 1, 1, 0.5, 0], [0, 1, 1, 0, -0.5, 0]])  # house-like arrow shape
house = np.array([[0, 1, 1, 0.5, 0, 0], [0, 0, 1, 1.5, 1, 0]], float)
steps = [("Original", np.eye(2)), ("Shear first", S), ("then rotate: R S", R @ S),
         ("Rotate first", R), ("then shear: S R", S @ R)]
fig, axes = plt.subplots(1, 5, figsize=(15, 3.6))
cols = [BLUE, ORANGE, TEAL, ORANGE, PURPLE]
for ax, (name, M), c in zip(axes, steps, cols):
    p = M @ house
    ax.fill(p[0], p[1], color=c, alpha=0.35)
    ax.plot(p[0], p[1], color=c, lw=2)
    ax.plot(*(M @ [0.5, 1.5]), "o", color=RED, ms=6)
    ax.set_xlim(-3, 3); ax.set_ylim(-1.5, 3); ax.set_aspect("equal"); ax.grid(alpha=0.3)
    ax.set_title(name, fontsize=10)
fig.suptitle("Order matters: R S is not S R (red dot marks the roof tip)", fontsize=12)
fig.tight_layout()
fig.savefig("ch06_compose.png", dpi=110)
