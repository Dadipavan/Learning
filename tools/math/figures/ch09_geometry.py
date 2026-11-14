import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
A = np.array([[3., 0.], [4., 5.]])
U, s, Vt = np.linalg.svd(A)
t = np.linspace(0, 2*np.pi, 200)
circle = np.vstack([np.cos(t), np.sin(t)])
steps = [circle, Vt @ circle, np.diag(s) @ Vt @ circle, U @ np.diag(s) @ Vt @ circle]
titles = ["Unit circle", "After Vᵀ (rotate/reflect)", "After S (stretch)", "After U (rotate): A x"]
fig, axs = plt.subplots(1, 4, figsize=(11, 3.3))
for ax, p, ti in zip(axs, steps, titles):
    ax.plot(p[0], p[1], color="#2b4fd6", lw=2)
    ax.plot(p[0][:1], p[1][:1], "o", color="#b84a22")
    ax.axhline(0, color="#999", lw=.6); ax.axvline(0, color="#999", lw=.6)
    ax.set_xlim(-7.5, 7.5); ax.set_ylim(-7.5, 7.5); ax.set_aspect("equal")
    ax.set_title(ti, fontsize=9)
    ax.tick_params(labelsize=7)
fig.suptitle("A = U S Vᵀ for A = [[3, 0], [4, 5]]: singular values %.3f and %.3f" % tuple(s), fontsize=10)
fig.tight_layout()
fig.savefig("ch09_geometry.png", dpi=110)
