import numpy as np
rng = np.random.default_rng(0); n = 40000
x = rng.normal(size=n); T = rng.integers(0, 2, n)
tau = np.where(x > 0, 0.10, -0.04)                      # persuadable if x>0, sleeping-dog otherwise
p = 0.10 + tau * T; y = rng.random(n) < p
from sklearn.ensemble import GradientBoostingClassifier as G
X = x[:, None]; m1 = G(max_depth=2, n_estimators=50, random_state=0).fit(X[T==1], y[T==1]); m0 = G(max_depth=2, n_estimators=50, random_state=0).fit(X[T==0], y[T==0])
up = m1.predict_proba(X)[:, 1] - m0.predict_proba(X)[:, 1]
print("true mean effect", round(tau.mean(), 3), " mean predicted uplift", up.mean().round(3))
order = np.argsort(-up)
for q in (0.25, 0.5, 1.0):
    k = order[: int(q * n)]; a = y[k][T[k]==1].mean() - y[k][T[k]==0].mean()
    print(f"top {int(q*100)}% by uplift: observed effect {a:.3f}")
r = np.argsort(-(m0.predict_proba(X)[:,1]))   # wrong: target by response propensity
k = r[: n // 4]; print("top 25% by baseline response: effect", round(y[k][T[k]==1].mean() - y[k][T[k]==0].mean(), 3))
