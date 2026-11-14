import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, SimpleImputer
rng = np.random.default_rng(0); n = 1000
age = rng.normal(40, 10, n); inc = 2 * age + rng.normal(0, 5, n); X = np.c_[age, inc]
mask = rng.random(n) < 0.3                      # income missing at random
Xm = X.copy(); Xm[mask, 1] = np.nan
true = X[mask, 1]
for name, imp in [("mean", SimpleImputer()), ("iterative", IterativeImputer(random_state=0))]:
    Z = imp.fit_transform(Xm)
    print(name, "RMSE", round(np.sqrt(np.mean((Z[mask, 1] - true) ** 2)), 2),
          "std of income", round(Z[:, 1].std(), 2), "corr(age,income)", round(np.corrcoef(Z.T)[0, 1], 3))
print("truth: std", round(X[:, 1].std(), 2), "corr", round(np.corrcoef(X.T)[0, 1], 3))
# MICE with sample_posterior: m=5 imputations, Rubin pooling of mean income
ests, vars_ = [], []
for s in range(5):
    Z = IterativeImputer(sample_posterior=True, random_state=s).fit_transform(Xm)[:, 1]
    ests.append(Z.mean()); vars_.append(Z.var(ddof=1) / n)
ests = np.array(ests); W = np.mean(vars_); B = ests.var(ddof=1); T = W + (1 + 1/5) * B
print("pooled mean", ests.mean().round(2), "within", round(W, 4), "between", round(B, 4), "total SE", round(T ** .5, 3))
