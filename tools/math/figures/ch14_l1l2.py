import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 11})

c = np.array([2.4, 0.3])                       # unconstrained optimum of the data loss
A = np.array([[1.0, 0.3], [0.3, 1.5]])
X, Y = np.meshgrid(np.linspace(-2.5, 3.5, 400), np.linspace(-2.2, 2.6, 400))
D = np.stack([X - c[0], Y - c[1]])
Z = A[0, 0] * D[0] ** 2 + 2 * A[0, 1] * D[0] * D[1] + A[1, 1] * D[1] ** 2
t = np.linspace(0, 2 * np.pi, 400)
fig, ax = plt.subplots(1, 2, figsize=(10, 4.4))
for a in ax:
    a.contour(X, Y, Z, levels=[0.3, 1, 2, 3.5, 5.5], colors="#bbbbbb", linewidths=1)
    a.axhline(0, color="#999", lw=0.8); a.axvline(0, color="#999", lw=0.8)
    a.plot(*c, marker="*", color=TEAL, ms=13, label="unconstrained best"); a.set_aspect("equal")
    a.set_xlabel("w1"); a.set_ylabel("w2")
def loss(p):
    d = p - c
    return A[0, 0] * d[0] ** 2 + 2 * A[0, 1] * d[0] * d[1] + A[1, 1] * d[1] ** 2
# brute-force check that the best point of the diamond is the corner (1.4, 0)
tt = np.linspace(0, 1, 2001)
edge = np.stack([r1 * (1 - tt), r1 * tt]) if False else None
# L1 ball |w1| + |w2| <= 1.4 : optimum at corner (1.4, 0)
r1 = 1.4
edge = np.stack([r1 * (1 - np.linspace(0, 1, 2001)), r1 * np.linspace(0, 1, 2001)])
print('best on edge at y =', edge[1][np.argmin([loss(edge[:, i]) for i in range(2001)])])
ax[0].fill([r1, 0, -r1, 0], [0, r1, 0, -r1], color=BLUE, alpha=0.25)
ax[0].plot([r1, 0, -r1, 0, r1], [0, r1, 0, -r1, 0], color=BLUE, lw=2)
ax[0].plot(r1, 0, "o", color=RED, ms=9, label="constrained best: w2 = 0")
ax[0].set_title("L1 constraint (diamond): corner, w2 = 0"); ax[0].legend(fontsize=8, loc="upper left")
# L2 ball: circle radius 1.4, optimum on the circle toward c, found numerically
r2 = 1.4
ax[1].fill(r2 * np.cos(t), r2 * np.sin(t), color=ORANGE, alpha=0.25)
ax[1].plot(r2 * np.cos(t), r2 * np.sin(t), color=ORANGE, lw=2)
pts = np.stack([r2 * np.cos(t), r2 * np.sin(t)])
d = pts - c[:, None]
val = A[0, 0] * d[0] ** 2 + 2 * A[0, 1] * d[0] * d[1] + A[1, 1] * d[1] ** 2
k = np.argmin(val)
ax[1].plot(pts[0, k], pts[1, k], "o", color=RED, ms=9, label="constrained best: both nonzero")
ax[1].set_title("L2 constraint (circle): both weights nonzero"); ax[1].legend(fontsize=8, loc="upper left")
plt.tight_layout(); plt.savefig("ch14_l1l2.png", dpi=110)
