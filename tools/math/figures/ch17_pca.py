import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BL, OR, TE, RD, PU = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

import numpy as np

rng = np.random.default_rng(7)
n = 500
names = ["monthly_spend", "orders", "avg_basket", "discount_use", "site_visits",
         "session_min", "app_opens", "tenure_months", "account_days", "support_tickets"]
L = np.array([[0.9, 0.1, 0.0], [0.7, 0.4, 0.0], [0.8, -0.3, 0.0], [-0.3, 0.2, 0.1],
              [0.1, 0.9, 0.0], [0.0, 0.8, 0.1], [0.1, 0.85, -0.1], [0.0, 0.1, 0.95],
              [0.0, 0.1, 0.95], [0.1, 0.2, 0.4]])
F = rng.normal(size=(n, 3))
X = 50 + (F @ L.T + 0.4 * rng.normal(size=(n, 10))) * np.array([120, 8, 35, 0.2, 20, 15, 30, 24, 730, 2])
Z = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)

vals, vecs = np.linalg.eigh(Z.T @ Z / (n - 1))
vals, vecs = vals[::-1], vecs[:, ::-1]
ratio = vals / vals.sum()
scores = Z @ vecs
fig, ax = plt.subplots(1, 2, figsize=(9, 4.2))
ax[0].bar(range(1, 11), ratio, color=BL, label="each component")
ax[0].plot(range(1, 11), np.cumsum(ratio), "o-", color=OR, label="cumulative")
ax[0].axhline(0.8, color="grey", ls="--", lw=1)
ax[0].set_xlabel("component"); ax[0].set_ylabel("share of variance"); ax[0].set_title("Scree plot"); ax[0].legend(loc="center right")
sc = ax[1].scatter(scores[:, 0], scores[:, 2], c=scores[:, 1], cmap="viridis", s=12)
ax[1].set_xlabel("PC1 score"); ax[1].set_ylabel("PC3 score"); ax[1].set_title("Customers on PC1 and PC3 (colour = PC2)")
fig.colorbar(sc, ax=ax[1], label="PC2 score")
plt.tight_layout(); plt.savefig("ch17_pca.png", dpi=110)
