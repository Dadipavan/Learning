import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
mats = [("Positive definite: eigenvalues 3, 1\nbowl, one minimum", np.array([[2., 1.], [1., 2.]])),
        ("Indefinite: eigenvalues 3, -1\nsaddle", np.array([[1., 2.], [2., 1.]])),
        ("Semi-definite: eigenvalues 2, 0\nflat valley", np.array([[1., 1.], [1., 1.]]))]
g = np.linspace(-2, 2, 200); X, Y = np.meshgrid(g, g)
fig, axs = plt.subplots(1, 3, figsize=(11, 4))
for ax, (title, S) in zip(axs, mats):
    Z = S[0, 0] * X**2 + 2 * S[0, 1] * X * Y + S[1, 1] * Y**2
    cs = ax.contourf(X, Y, Z, levels=14, cmap="RdBu_r", vmin=-np.abs(Z).max(), vmax=np.abs(Z).max())
    ax.contour(X, Y, Z, levels=[0], colors="k", linewidths=1.2)
    w, V = np.linalg.eigh(S)
    for lam, v, c in zip(w, V.T, ["#6a2fd0", "#357a70"]):
        ax.plot([-2 * v[0], 2 * v[0]], [-2 * v[1], 2 * v[1]], color=c, lw=2, ls="--")
    ax.set_title(title, fontsize=10); ax.set_aspect("equal")
plt.tight_layout(); plt.savefig("ch08_quadform.png", dpi=110)
