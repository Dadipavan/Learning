import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(8, 4.2))
c = np.array([2.0, 0.3])  # unconstrained optimum of the loss
t = np.linspace(0, 2*np.pi, 400)
gx, gy = np.meshgrid(np.linspace(-1.3, 3.2, 300), np.linspace(-1.5, 2, 300))
loss = (gx-c[0])**2 + 1.5*(gy-c[1])**2
for ax, kind in zip(axes, ["L1", "L2"]):
    ax.contour(gx, gy, loss, levels=[0.2, 0.6, 1.2, 2.0], colors="#2b4fd6", linewidths=1)
    if kind == "L1":
        ax.fill([1, 0, -1, 0], [0, 1, 0, -1], color="#b84a22", alpha=0.25)
        ax.plot([1, 0, -1, 0, 1], [0, 1, 0, -1, 0], color="#b84a22")
        ax.plot([1], [0], "o", color="#aa2d26", ms=8); ax.annotate("solution on a corner:\nw2 = 0 (sparse)", (1, 0), (1.05, -1.2), fontsize=8)
        ax.set_title("L1 constraint |w1| + |w2| <= 1 (diamond)")
    else:
        ax.fill(np.cos(t), np.sin(t), color="#357a70", alpha=0.25)
        ax.plot(np.cos(t), np.sin(t), color="#357a70")
        pts = np.stack([np.cos(t), np.sin(t)], 1)
        d = pts[np.argmin((pts[:,0]-c[0])**2 + 1.5*(pts[:,1]-c[1])**2)]
        ax.plot([d[0]], [d[1]], "o", color="#aa2d26", ms=8); ax.annotate("smooth boundary:\nboth weights nonzero", d, (0.2, -1.2), fontsize=8)
        ax.set_title("L2 constraint w1^2 + w2^2 <= 1 (circle)")
    ax.plot(*c, "k*", ms=10); ax.set_aspect("equal"); ax.set_xlim(-1.3, 3.2); ax.set_ylim(-1.5, 2)
    ax.set_xlabel("w1"); ax.set_ylabel("w2"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("ch16_l1_l2_geometry.png", dpi=110)
