import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = np.array([[5, 4, np.nan, 1, 1], [4, np.nan, 5, 1, 2], [5, 5, 4, np.nan, 1],
              [1, 1, np.nan, 5, 4], [2, np.nan, 1, 4, 5], [1, 2, 1, 5, np.nan]])
M = ~np.isnan(R); k = 2; lam = 0.1
rng = np.random.default_rng(0)
P = rng.normal(0, 0.5, (6, k)); Q = rng.normal(0, 0.5, (5, k))
hist = []
for it in range(25):
    for u in range(6):
        Qi = Q[M[u]]; P[u] = np.linalg.solve(Qi.T @ Qi + lam*np.eye(k), Qi.T @ R[u, M[u]])
    for i in range(5):
        Pu = P[M[:, i]]; Q[i] = np.linalg.solve(Pu.T @ Pu + lam*np.eye(k), Pu.T @ R[M[:, i], i])
    hist.append(np.sqrt(np.mean((P @ Q.T - R)[M]**2)))
fig, axs = plt.subplots(1, 2, figsize=(9, 3.8))
axs[0].plot(range(1, 26), hist, "o-", color="#2b4fd6", ms=4)
axs[0].set_xlabel("ALS sweep"); axs[0].set_ylabel("RMSE on known ratings"); axs[0].set_title("ALS training error")
im = axs[1].imshow(P @ Q.T, cmap="viridis", vmin=1, vmax=5)
for u in range(6):
    for i in range(5):
        if not M[u, i]: axs[1].text(i, u, "?", ha="center", va="center", color="white", fontsize=14, fontweight="bold")
axs[1].set_title("Completed matrix (? = was missing)"); axs[1].set_xlabel("movie"); axs[1].set_ylabel("user")
fig.colorbar(im, ax=axs[1], fraction=0.046)
fig.tight_layout(); fig.savefig("ch09_als.png", dpi=110)
