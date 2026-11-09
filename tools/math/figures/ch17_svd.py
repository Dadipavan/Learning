import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BL, OR, TE, RD, PU = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

import numpy as np

def make_image(size=96, seed=2):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size] / (size - 1)
    img = 0.3 + 0.4 * xx * yy                                    # smooth gradient
    img += 0.25 * (((xx - 0.65) ** 2 + (yy - 0.35) ** 2) < 0.04)  # a disc
    img += 0.15 * ((np.sin(18 * xx) > 0.3) & (yy > 0.7))           # stripes in the lower band
    img += 0.2 * ((abs(xx - 0.2) < 0.07) & (yy < 0.6))             # a bar
    img += 0.02 * rng.normal(size=(size, size))                    # sensor noise
    return np.clip(img, 0, 1)

rng = np.random.default_rng(4)
n_users, n_items, true_rank = 120, 50, 3
Uf = rng.normal(size=(n_users, true_rank))
Vf = rng.normal(size=(n_items, true_rank))
full = np.clip(3.2 + 0.7 * (Uf @ Vf.T) + 0.3 * rng.normal(size=(n_users, n_items)), 1, 5)   # "true" ratings
mask = rng.random((n_users, n_items)) < 0.25                                          # 25% observed
test_mask = (~mask) & (rng.random((n_users, n_items)) < 0.25)                          # held-out cells
def als(k, lam, iters=25, seed=0):
    r = np.random.default_rng(seed)
    mu = full[mask].mean()
    Pu, Qi = 0.1 * r.normal(size=(n_users, k)), 0.1 * r.normal(size=(n_items, k))
    R = full - mu
    for _ in range(iters):
        for u in range(n_users):                         # fix items, solve ridge for each user
            idx = mask[u]
            Qs = Qi[idx]
            Pu[u] = np.linalg.solve(Qs.T @ Qs + lam * np.eye(k), Qs.T @ R[u, idx])
        for i in range(n_items):                         # fix users, solve ridge for each item
            idx = mask[:, i]
            Ps = Pu[idx]
            Qi[i] = np.linalg.solve(Ps.T @ Ps + lam * np.eye(k), Ps.T @ R[idx, i])
    return mu + Pu @ Qi.T

rmse = lambda pred, m: np.sqrt(np.mean((pred[m] - full[m]) ** 2))

img = make_image(); U, S, Vt = np.linalg.svd(img, full_matrices=False)
fig = plt.figure(figsize=(9.5, 6.4)); gs = fig.add_gridspec(2, 3)
for c, k in enumerate([2, 10, 40]):
    a = fig.add_subplot(gs[0, c]); a.imshow((U[:, :k] * S[:k]) @ Vt[:k], cmap="gray", vmin=0, vmax=1)
    a.set_title(f"rank {k} ({k * 193 / 96**2:.0%} of numbers)"); a.axis("off")
a = fig.add_subplot(gs[1, :2]); ks = np.arange(1, 61)
rel = np.array([np.sqrt((S[k:] ** 2).sum() / (S**2).sum()) for k in ks])
a.semilogy(ks, rel, color=BL, label="relative error (Eckart-Young)")
a.semilogy(ks, S[:60] / S[0], color=OR, ls="--", label="singular value / largest")
a.set_xlabel("rank k"); a.set_title("Image: error vs rank"); a.legend(fontsize=8)
a = fig.add_subplot(gs[1, 2]); rk = [1, 2, 3, 4, 6, 8]
tr = []; te = []
for k in rk:
    p = als(k, 0.5); tr.append(rmse(p, mask)); te.append(rmse(p, test_mask))
a.plot(rk, tr, "o-", color=TE, label="train"); a.plot(rk, te, "o-", color=RD, label="held-out")
a.axhline(rmse(np.full_like(full, full[mask].mean()), test_mask), color="grey", ls=":", label="global mean")
a.set_xlabel("latent rank"); a.set_ylabel("RMSE"); a.set_title("Recommender: RMSE vs rank"); a.legend(fontsize=8)
plt.tight_layout(); plt.savefig("ch17_svd.png", dpi=110)
