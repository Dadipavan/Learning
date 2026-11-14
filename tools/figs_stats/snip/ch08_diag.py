import numpy as np
from sklearn.linear_model import LogisticRegression
from scipy.stats import chi2
rng = np.random.default_rng(84)
n = 2000
X = rng.normal(0, 1, (n, 2))
p = 1 / (1 + np.exp(-(-1.0 + 1.1 * X[:, 0] + 0.6 * X[:, 1])))
y = (rng.random(n) < p).astype(int)
tr, te = slice(0, 1200), slice(1200, n)
m = LogisticRegression(C=1e6).fit(X[tr], y[tr])
ph = m.predict_proba(X[te])[:, 1]; yt = y[te]
def auc(s, yy):
    r = s.argsort().argsort() + 1
    n1 = yy.sum(); n0 = len(yy) - n1
    return (r[yy == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
print("test AUC:", round(auc(ph, yt), 3))
# Hosmer-Lemeshow on the training data (g - 2 = 8 df), 10 equal-count groups
ptr = m.predict_proba(X[tr])[:, 1]; ytr = y[tr]
o = np.argsort(ptr); groups = np.array_split(o, 10)
hl = 0
for g in groups:
    n_g, obs, exp = len(g), ytr[g].sum(), ptr[g].sum()
    pbar = exp / n_g
    hl += (obs - exp) ** 2 / (n_g * pbar * (1 - pbar))
print(f"Hosmer-Lemeshow chi2 = {hl:.2f} on 8 df, p = {1 - chi2.cdf(hl, 8):.3f}")
print("decile  mean predicted  observed rate")
for i, g in enumerate(groups):
    print(f"{i+1:>6}  {ptr[g].mean():>14.3f}  {ytr[g].mean():>13.3f}")
# separation
xs = np.concatenate([rng.normal(-2, .3, 50), rng.normal(2, .3, 50)]).reshape(-1, 1); ys = np.r_[np.zeros(50), np.ones(50)]
print("perfect separation, slope as the penalty weakens:")
for C in [1, 100, 1e4, 1e6]:
    print(f"  C = {C:>9g}: slope = {LogisticRegression(C=C, max_iter=5000).fit(xs, ys).coef_[0][0]:.2f}")
