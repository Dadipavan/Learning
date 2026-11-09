import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
A = np.array([[4., 1.], [2., 3.]])
fig, axs = plt.subplots(1, 2, figsize=(9, 4.4))
lines = np.linspace(-2, 2, 9)
t = np.linspace(-2, 2, 50)
for ax, M, title in [(axs[0], np.eye(2), "Before: the unit grid"), (axs[1], A, "After: apply A")]:
    for c in lines:
        h = M @ np.vstack([t, np.full_like(t, c)])
        v = M @ np.vstack([np.full_like(t, c), t])
        ax.plot(h[0], h[1], color="#c9cfdd", lw=0.9)
        ax.plot(v[0], v[1], color="#c9cfdd", lw=0.9)
    for vec, col, name in [(np.array([1., 1.]), "#2b4fd6", "v1 = (1, 1)"), (np.array([1., -2.]), "#b84a22", "v2 = (1, -2)")]:
        w = M @ vec
        ax.annotate("", xy=w, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4))
        ax.plot([-4 * vec[0], 4 * vec[0]], [-4 * vec[1], 4 * vec[1]], color=col, lw=0.8, ls="--")
    ax.set_xlim(-6, 6); ax.set_ylim(-6, 6); ax.set_aspect("equal"); ax.axhline(0, color="k", lw=.5); ax.axvline(0, color="k", lw=.5)
    ax.set_title(title, fontsize=12)
axs[1].text(0.5, 5.2, "A v1 = 5 v1 (stretched x5)", color="#2b4fd6", fontsize=9)
axs[1].text(-5.8, -5.5, "A v2 = 2 v2 (stretched x2)", color="#b84a22", fontsize=9)
plt.tight_layout(); plt.savefig("ch08_grid.png", dpi=110)
