import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rng = np.random.default_rng(8)
Z = rng.normal(size=(300, 2)) * np.array([3.0, 1.0])
th = np.pi / 6
R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
X = Z @ R.T + np.array([2, 1])
S = np.cov(X.T)
w, V = np.linalg.eigh(S)
V = V * np.sign(V[0:1, :] + 1e-12)
mu = X.mean(0)
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(X[:, 0], X[:, 1], s=10, color="#2b4fd6", alpha=.5)
a = np.linspace(0, 2 * np.pi, 200)
E = (V @ np.diag(np.sqrt(w)) @ np.vstack([np.cos(a), np.sin(a)])).T * 2 + mu
ax.plot(E[:, 0], E[:, 1], color="#aa2d26", lw=1.5)
for lam, v, c, n in [(w[1], V[:, 1], "#b84a22", "PC1"), (w[0], V[:, 0], "#357a70", "PC2")]:
    ax.annotate("", xy=mu + 2 * np.sqrt(lam) * v, xytext=mu, arrowprops=dict(arrowstyle="-|>", color=c, lw=2.5))
    ax.text(*(mu + 2.15 * np.sqrt(lam) * v + np.array([0.1, 0.1])), f"{n}: variance {lam:.2f}", color=c, fontsize=10)
ax.set_aspect("equal"); ax.set_title("Eigenvectors of the covariance matrix point along the spread")
ax.set_xlabel("feature 1"); ax.set_ylabel("feature 2")
plt.tight_layout(); plt.savefig("ch08_cov_ellipse.png", dpi=110)
