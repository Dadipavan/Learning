import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(42)
n = 20000
age = rng.normal(35, 8, n)
tenure = rng.exponential(12, n)
activity = rng.normal(0, 1, n)
# who gets the premium feature depends on covariates (confounding)
logit = -1.0 + 0.9 * activity + 0.04 * (tenure - 12) + 0.02 * (age - 35)
t = rng.random(n) < 1 / (1 + np.exp(-logit))
# outcome: spend. True causal effect of the feature = +2.0
y = 20 + 4 * activity + 0.3 * tenure + 0.1 * age + 2.0 * t + rng.normal(0, 5, n)
X = np.column_stack([age, tenure, activity])
Z = (X - X.mean(0)) / X.std(0)
def smd(a, b, wa=None, wb=None):
    wa = np.ones(len(a)) if wa is None else wa; wb = np.ones(len(b)) if wb is None else wb
    ma, mb = np.average(a, weights=wa), np.average(b, weights=wb)
    va, vb = np.average((a-ma)**2, weights=wa), np.average((b-mb)**2, weights=wb)
    return (ma - mb) / np.sqrt((va + vb) / 2)
print("naive difference      :", round(y[t].mean() - y[~t].mean(), 3))
# regression adjustment
A = np.column_stack([np.ones(n), t, X]); b = np.linalg.lstsq(A, y, rcond=None)[0]
print("regression adjusted   :", round(b[1], 3))
# propensity score
ps = LogisticRegression(C=1e6, max_iter=1000).fit(Z, t).predict_proba(Z)[:, 1]
print("propensity range      :", round(ps.min(), 3), round(ps.max(), 3))
# inverse probability weighting (stabilised)
w = np.where(t, t.mean() / ps, (1 - t.mean()) / (1 - ps))
ipw = np.average(y[t], weights=w[t]) - np.average(y[~t], weights=w[~t])
print("IPW                   :", round(ipw, 3))
# balance table: standardized mean difference before and after weighting
print("covariate   SMD raw  SMD weighted")
for j, name in enumerate(["age", "tenure", "activity"]):
    raw = smd(X[t, j], X[~t, j]); wt = smd(X[t, j], X[~t, j], w[t], w[~t])
    print(f"{name:10s} {raw:7.3f} {wt:9.3f}")
# 1-nearest-neighbour matching on the propensity score (treated matched to controls, with replacement)
lp = np.log(ps / (1 - ps))
ct = np.where(~t)[0]; tr = np.where(t)[0]
order = np.argsort(lp[ct]); sorted_lp = lp[ct][order]
pos = np.clip(np.searchsorted(sorted_lp, lp[tr]), 1, len(ct) - 1)
left, right = sorted_lp[pos - 1], sorted_lp[pos]
pick = np.where(np.abs(lp[tr] - left) <= np.abs(lp[tr] - right), pos - 1, pos)
matched = ct[order][pick]
print("matching ATT          :", round((y[tr] - y[matched]).mean(), 3))
