import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
th = np.deg2rad(30)
mats = [
    ("Rotation 30°", np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])),
    ("Scaling (2, 0.5)", np.array([[2.0, 0], [0, 0.5]])),
    ("Shear (k = 1)", np.array([[1.0, 1], [0, 1]])),
    ("Reflection (x-axis)", np.array([[1.0, 0], [0, -1]])),
    ("Projection onto x-axis", np.array([[1.0, 0], [0, 0]])),
]
fig, axes = plt.subplots(2, 5, figsize=(14, 6.2))
t = np.linspace(0, 2 * np.pi, 200)
circle = np.vstack([np.cos(t), np.sin(t)])
square = np.array([[0, 1, 1, 0, 0], [0, 0, 1, 1, 0]], float)
for j, (name, M) in enumerate(mats):
    for i in range(2):
        ax = axes[i, j]
        A = np.eye(2) if i == 0 else M
        for g in np.arange(-3, 4):
            line = np.array([[g, g], [-3, 3]], float)
            l1 = A @ line
            l2 = A @ line[::-1]
            ax.plot(l1[0], l1[1], color="#cccccc", lw=0.8)
            ax.plot(l2[0], l2[1], color="#cccccc", lw=0.8)
        s = A @ square
        c = A @ circle
        ax.fill(s[0], s[1], color=ORANGE, alpha=0.35)
        ax.plot(s[0], s[1], color=ORANGE, lw=1.8)
        ax.plot(c[0], c[1], color=BLUE, lw=1.8)
        ax.annotate("", xy=A @ [1, 0], xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=RED, lw=2))
        ax.annotate("", xy=A @ [0, 1], xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
        ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect("equal")
        ax.set_xticks([-2, 0, 2]); ax.set_yticks([-2, 0, 2]); ax.tick_params(labelsize=8)
        ax.set_title(("Before" if i == 0 else name), fontsize=10)
fig.suptitle("Five 2x2 transformations: red arrow = image of e1, teal arrow = image of e2", fontsize=12)
fig.tight_layout()
fig.savefig("ch06_transforms.png", dpi=110)
