import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BL, OR, TE, RD, PU = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

import numpy as np

rng = np.random.default_rng(11)
n_train, n_test, p = 25, 500, 8
shared = rng.normal(size=(n_train + n_test, 1))
X = 0.9 * shared + 0.45 * rng.normal(size=(n_train + n_test, p))     # correlated features (r about 0.8)
beta_true = np.array([3.0, -2.0, 0.0, 0.0, 1.5, 0.0, 0.0, -1.0])
y = 5.0 + X @ beta_true + 3.0 * rng.normal(size=n_train + n_test)
Xtr, ytr, Xte, yte = X[:n_train], y[:n_train], X[n_train:], y[n_train:]

mu, sd = Xtr.mean(axis=0), Xtr.std(axis=0)
Xs, Xt = (Xtr - mu) / sd, (Xte - mu) / sd
yc = ytr - ytr.mean()
w_exact = np.linalg.lstsq(Xs, yc, rcond=None)[0]
H = Xs.T @ Xs / n_train
eigs = np.linalg.eigvalsh(H); L_, mu_ = eigs.max(), eigs.min()

fig, ax = plt.subplots(1, 2, figsize=(9.5, 4.2))
for lr, col in [(0.05, BL), (0.2, TE), (2 / (L_ + mu_), PU), (0.5, RD)]:
    w, errs = np.zeros(8), []
    for t in range(600):
        w = w - lr * Xs.T @ (Xs @ w - yc) / n_train
        errs.append(np.linalg.norm(w - w_exact))
    ax[0].semilogy(errs, color=col, label=f"lr = {lr:.2f}" + (" (best)" if col == PU else ""))
ax[0].axhline(1e-6, color="grey", ls=":")
ax[0].set_ylim(1e-7, 1e4); ax[0].set_xlim(0, 600)
ax[0].set_xlabel("step"); ax[0].set_ylabel("distance to exact answer"); ax[0].set_title("Gradient descent: learning-rate study"); ax[0].legend(fontsize=8)

U, s, Vt = np.linalg.svd(Xs, full_matrices=False)
lams = np.logspace(-2, 3.5, 60)
W = np.array([Vt.T @ ((s / (s**2 + l)) * (U.T @ yc)) for l in lams])
cols = [BL, OR, TE, RD, PU, "#555555", "#999900", "#cc79a7"]
for j in range(8):
    ax[1].plot(lams, W[:, j], color=cols[j], label=f"x{j+1} (true {beta_true[j]:g})")
ax[1].set_xscale("log"); ax[1].axhline(0, color="k", lw=0.5)
ax[1].set_xlabel("lambda"); ax[1].set_ylabel("standardised coefficient"); ax[1].set_title("Ridge regularization path"); ax[1].legend(fontsize=7, ncol=2)
plt.tight_layout(); plt.savefig("ch17_regression.png", dpi=110)
