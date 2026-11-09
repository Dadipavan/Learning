import numpy as np
from scipy.stats import chi2
rng = np.random.default_rng(7)
n, phi = 300, 0.6
e = rng.normal(0, 1, n); y = np.zeros(n)
for t in range(1, n): y[t] = phi * y[t-1] + e[t]
def acf(x, k):
    x = x - x.mean(); d = np.dot(x, x)
    return np.array([np.dot(x[:len(x)-l], x[l:]) / d for l in range(1, k + 1)])
def ljung_box(res, h, n_params=0):
    r = acf(res, h); N = len(res)
    Q = N * (N + 2) * np.sum(r ** 2 / (N - np.arange(1, h + 1)))
    return Q, 1 - chi2.cdf(Q, h - n_params)
res_mean = y - y.mean()                                       # model 1: "just a mean"
phi_hat = np.dot(y[1:] - y.mean(), y[:-1] - y.mean()) / np.dot(y[:-1] - y.mean(), y[:-1] - y.mean())
res_ar = (y[1:] - y.mean()) - phi_hat * (y[:-1] - y.mean())   # model 2: AR(1)
print("residual ACF at lags 1-3, mean-only model:", np.round(acf(res_mean, 3), 3))
print("residual ACF at lags 1-3, AR(1) model    :", np.round(acf(res_ar, 3), 3))
print(f"phi_hat = {phi_hat:.3f} (true 0.6); 95% white-noise band for the ACF = +/- {1.96/np.sqrt(n):.3f}")
Q, p = ljung_box(res_mean, 10); print(f"Ljung-Box, mean-only, 10 lags: Q = {Q:.1f}, p < 0.0001" if p < 1e-4 else f"Ljung-Box, mean-only: Q = {Q:.1f}, p = {p:.3f}")
Q, p = ljung_box(res_ar, 10, 1); print(f"Ljung-Box, AR(1),     10 lags: Q = {Q:.1f}, p = {p:.3f}  (df = 10 - 1 fitted parameter)")
