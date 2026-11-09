import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 10})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
cols = [B, O, T, P, R]
# ch13: DBSCAN vs HDBSCAN
from sklearn.cluster import DBSCAN, HDBSCAN
from sklearn.datasets import make_blobs
rng = np.random.default_rng(0)
X1, y1 = make_blobs(n_samples=[200, 200], centers=[[0, 0], [6, 0]], cluster_std=[0.3, 1.5], random_state=0)
X = np.r_[X1, rng.uniform(-3, 9, (40, 2))]
labs = [("DBSCAN eps=0.6", DBSCAN(eps=0.6, min_samples=10).fit_predict(X)), ("DBSCAN eps=1.0", DBSCAN(eps=1.0, min_samples=10).fit_predict(X)),
        ("HDBSCAN min_cluster_size=30", HDBSCAN(min_cluster_size=30, copy=True).fit_predict(X))]
fig, ax = plt.subplots(1, 3, figsize=(11, 3.6), dpi=110, sharex=True, sharey=True)
for a, (t, l) in zip(ax, labs):
    for c in sorted(set(l)):
        m = l == c; a.scatter(X[m, 0], X[m, 1], s=9, c="#999999" if c == -1 else cols[c % 5], marker="x" if c == -1 else "o")
    a.set_title(t + f"\nclusters {len(set(l)-{-1})}, noise {(l==-1).sum()}")
plt.tight_layout(); plt.savefig("ch13_hdbscan.png"); plt.close()
# ch06: tree + regions
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
Xi, yi = load_iris(return_X_y=True); Xi = Xi[:, 2:]
t = DecisionTreeClassifier(max_depth=3, random_state=0).fit(Xi, yi)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6), dpi=110, gridspec_kw={"width_ratios": [1.5, 1]})
plot_tree(t, feature_names=["petal_len", "petal_wid"], class_names=["setosa", "versicolor", "virginica"], filled=True, impurity=True, ax=ax[0], fontsize=7)
gx, gy = np.meshgrid(np.linspace(0.8, 7, 300), np.linspace(0, 2.7, 300))
ax[1].contourf(gx, gy, t.predict(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape), levels=[-.5, .5, 1.5, 2.5], colors=["#dfe6fb", "#f3dccf", "#d3e9e4"])
for c in range(3): ax[1].scatter(Xi[yi == c, 0], Xi[yi == c, 1], s=14, c=cols[c])
ax[1].set_xlabel("petal length"); ax[1].set_ylabel("petal width"); ax[1].set_title("The same tree as rectangles")
plt.tight_layout(); plt.savefig("ch06_tree_view.png"); plt.close()
# ch08: split timelines
from sklearn.model_selection import KFold, GroupKFold, TimeSeriesSplit
n = 12; g = np.repeat(np.arange(4), 3)
fig, ax = plt.subplots(1, 3, figsize=(11, 3.2), dpi=110, sharey=True)
for a, (nm, sp, kw) in zip(ax, [("KFold(3)", KFold(3), {}), ("GroupKFold(3), 4 patients", GroupKFold(3), {"groups": g}), ("TimeSeriesSplit(3)", TimeSeriesSplit(3), {})]):
    for f, (tr, te) in enumerate(sp.split(np.zeros(n), **kw)):
        a.scatter(tr, [f] * len(tr), c=B, s=60, marker="s"); a.scatter(te, [f] * len(te), c=O, s=60, marker="s")
    a.set_title(nm); a.set_xlabel("row (time order)"); a.set_yticks(range(3))
    if nm.startswith("Group"):
        for x in (2.5, 5.5, 8.5): a.axvline(x, color="#999", lw=0.8, ls=":")
ax[0].set_ylabel("fold"); ax[0].scatter([], [], c=B, marker="s", label="train"); ax[0].scatter([], [], c=O, marker="s", label="test"); ax[0].legend(frameon=False, loc="lower right", fontsize=8)
plt.tight_layout(); plt.savefig("ch08_splits.png"); plt.close()
# ch02: BLR vs GP
r = np.random.default_rng(0)
x = np.linspace(-3, 3, 8); y = 1.0 + 2.0 * x + r.normal(0, 1.0, 8)
Phi = np.c_[np.ones_like(x), x]; S = np.linalg.inv(np.eye(2) + Phi.T @ Phi); m = S @ Phi.T @ y
xs = np.linspace(-8, 8, 200); F = np.c_[np.ones_like(xs), xs]; mu = F @ m; sd = np.sqrt(np.einsum("ij,jk,ik->i", F, S, F) + 1)
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel as C
xt = np.sort(r.uniform(-4, 4, 12)); yt = np.sin(xt) + r.normal(0, 0.15, 12)
gp = GPR(C(1.0) * RBF(1.0) + WhiteKernel(0.1), normalize_y=True, n_restarts_optimizer=5, random_state=0).fit(xt[:, None], yt)
g_mu, g_sd = gp.predict(xs[:, None], return_std=True)
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8), dpi=110)
ax[0].fill_between(xs, mu - 2 * sd, mu + 2 * sd, color=B, alpha=.2); ax[0].plot(xs, mu, c=B); ax[0].scatter(x, y, c=O, zorder=3)
ax[0].set_title("Bayesian linear regression: band flares at the ends"); ax[0].set_xlabel("x")
ax[1].fill_between(xs, g_mu - 2 * g_sd, g_mu + 2 * g_sd, color=T, alpha=.25); ax[1].plot(xs, g_mu, c=T); ax[1].scatter(xt, yt, c=O, zorder=3)
ax[1].plot(xs, np.sin(xs), c="#777", ls=":", label="truth"); ax[1].legend(frameon=False); ax[1].set_title("Gaussian process (RBF): band opens far from data"); ax[1].set_xlabel("x")
plt.tight_layout(); plt.savefig("ch02_blr_gp.png"); plt.close()
# ch16: KM + uplift
t_ = np.array([2, 3, 3, 5, 6, 8, 8, 9, 12, 12]); e_ = np.array([1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
ts, ss, S_ = [0], [1.0], 1.0
for u in np.unique(t_[e_ == 1]):
    S_ *= 1 - ((t_ == u) & (e_ == 1)).sum() / (t_ >= u).sum(); ts.append(u); ss.append(S_)
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8), dpi=110)
ax[0].step(ts + [12], ss + [ss[-1]], where="post", c=B, lw=2)
for tt, ee in zip(t_, e_):
    if not ee: ax[0].plot(tt, ss[np.searchsorted(ts, tt, side="right") - 1], "|", c=R, ms=14, mew=2)
ax[0].set_xlabel("time"); ax[0].set_ylabel("S(t)"); ax[0].set_title("Kaplan-Meier (red ticks = censored)")
rng2 = np.random.default_rng(0); n = 40000; xx = rng2.normal(size=n); Tt = rng2.integers(0, 2, n)
tau = np.where(xx > 0, .10, -.04); yy = rng2.random(n) < .10 + tau * Tt
from sklearn.ensemble import GradientBoostingClassifier as G
Xx = xx[:, None]; m1 = G(max_depth=2, n_estimators=50, random_state=0).fit(Xx[Tt == 1], yy[Tt == 1]); m0 = G(max_depth=2, n_estimators=50, random_state=0).fit(Xx[Tt == 0], yy[Tt == 0])
up = m1.predict_proba(Xx)[:, 1] - m0.predict_proba(Xx)[:, 1]; o = np.argsort(-up); qs = np.arange(.1, 1.01, .1); eff = []
for q in qs:
    k = o[:int(q * n)]; eff.append(yy[k][Tt[k] == 1].mean() - yy[k][Tt[k] == 0].mean())
ax[1].plot(qs * 100, eff, "o-", c=T); ax[1].axhline(tau.mean(), c=R, ls="--", label="treat everyone"); ax[1].legend(frameon=False)
ax[1].set_xlabel("% targeted (highest predicted uplift first)"); ax[1].set_ylabel("observed effect in targeted group"); ax[1].set_title("Uplift: target the persuadables")
plt.tight_layout(); plt.savefig("ch16_km_uplift.png"); plt.close()
