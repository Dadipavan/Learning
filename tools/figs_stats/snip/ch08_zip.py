import numpy as np
from scipy.optimize import minimize
from scipy.special import gammaln
rng = np.random.default_rng(81)
n = 2000
structural = rng.random(n) < 0.30          # never-buyers
y = np.where(structural, 0, rng.poisson(3.0, n))
print("share of zeros observed:", round((y == 0).mean(), 3), " mean:", round(y.mean(), 3), " variance:", round(y.var(), 3))
lam_p = y.mean()
print("Poisson with same mean predicts zeros:", round(np.exp(-lam_p), 3))

def nll(p):
    pi = 1 / (1 + np.exp(-p[0])); lam = np.exp(p[1])
    ll0 = np.log(pi + (1 - pi) * np.exp(-lam))
    llp = np.log(1 - pi) - lam + y * np.log(lam) - gammaln(y + 1)
    return -np.where(y == 0, ll0, llp).sum()
r = minimize(nll, [0.0, 0.5], method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-10})
pi, lam = 1 / (1 + np.exp(-r.x[0])), np.exp(r.x[1])
ll_pois = (-lam_p + y * np.log(lam_p) - gammaln(y + 1)).sum()
print(f"ZIP estimates: pi = {pi:.3f} (true 0.30), lambda = {lam:.3f} (true 3.00)")
print(f"AIC Poisson {2*1 - 2*ll_pois:.1f}   AIC ZIP {2*2 + 2*r.fun:.1f}")
