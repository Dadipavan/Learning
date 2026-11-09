import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rng = np.random.default_rng(1)
mu = np.array([2.0, 1.0]); S = np.array([[4.0, 2.4], [2.4, 2.0]])
L = np.linalg.cholesky(S)
X = mu + rng.standard_normal((600, 2)) @ L.T
vals, vecs = np.linalg.eigh(S)
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.scatter(X[:, 0], X[:, 1], s=9, color="#2b4fd6", alpha=0.45, label="600 samples via Cholesky")
t = np.linspace(0, 2*np.pi, 200)
for k, c in zip([1, 2], ["#357a70", "#6a2fd0"]):
    pts = mu[:, None] + k * vecs @ (np.sqrt(vals)[:, None] * np.array([np.cos(t), np.sin(t)]))
    ax.plot(pts[0], pts[1], color=c, lw=2, label=f"Mahalanobis distance {k}")
for i in range(2):
    v = vecs[:, i] * np.sqrt(vals[i])
    ax.arrow(mu[0], mu[1], 2*v[0], 2*v[1], color="#b84a22", width=0.04, length_includes_head=True)
    ax.text(mu[0] + 2.2*v[0], mu[1] + 2.2*v[1], f"eigenvector, variance {vals[i]:.2f}", color="#b84a22", fontsize=9)
ax.set_aspect("equal"); ax.set_xlabel("x1"); ax.set_ylabel("x2")
ax.set_title("Bivariate normal: contours are ellipses along the eigenvectors of the covariance")
ax.legend(loc="upper left", fontsize=8); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("ch15_mvn_ellipse.png", dpi=110)
