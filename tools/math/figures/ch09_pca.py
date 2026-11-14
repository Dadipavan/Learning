import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
X = np.array([[1, 2], [2, 3], [3, 5], [4, 4], [5, 6]], float)
mu = X.mean(0); Xc = X - mu
fig, axs = plt.subplots(1, 2, figsize=(9, 4.2))
ax = axs[0]
ax.scatter(X[:, 0], X[:, 1], color="#2b4fd6", s=45, zorder=3)
ax.plot(*mu, "k+", ms=12)
v1 = np.array([1, 1]) / np.sqrt(2); v2 = np.array([1, -1]) / np.sqrt(2)
ax.annotate("", xy=mu + 2.6*v1, xytext=mu, arrowprops=dict(arrowstyle="->", color="#b84a22", lw=2))
ax.annotate("", xy=mu + 1.2*v2, xytext=mu, arrowprops=dict(arrowstyle="->", color="#357a70", lw=2))
ax.text(*(mu + 2.8*v1), "PC1", color="#b84a22"); ax.text(*(mu + 1.3*v2), "PC2", color="#357a70")
for p in X:
    q = mu + ((p - mu) @ v1) * v1
    ax.plot([p[0], q[0]], [p[1], q[1]], color="#aa2d26", lw=1, ls=":")
ax.set_aspect("equal"); ax.set_xlim(0, 7); ax.set_ylim(0, 8); ax.set_title("Five points, centre (3, 4), principal axes")
ax.set_xlabel("x"); ax.set_ylabel("y")
ax = axs[1]
rng = np.random.default_rng(1)
vals = [4.75, 0.25]
ax.bar(["PC1", "PC2"], [v / 5 for v in vals], color=["#2b4fd6", "#357a70"])
ax.set_ylim(0, 1); ax.set_ylabel("explained variance ratio"); ax.set_title("Explained variance: 0.95 and 0.05")
for i, v in enumerate(vals): ax.text(i, v/5 + .02, "%.2f" % (v/5), ha="center")
fig.tight_layout(); fig.savefig("ch09_pca.png", dpi=110)
