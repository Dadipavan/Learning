import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2
rng = np.random.default_rng(105)
n = 2500; om, al, be = 0.05, 0.10, 0.85          # long-run variance = om / (1 - al - be) = 1.0
r = np.zeros(n); s2 = np.zeros(n); s2[0] = om / (1 - al - be)
for t in range(n):
    if t > 0: s2[t] = om + al * r[t-1] ** 2 + be * s2[t-1]
    r[t] = np.sqrt(s2[t]) * rng.normal()
def acf(x, k):
    x = x - x.mean(); d = np.dot(x, x); return np.array([np.dot(x[:len(x)-l], x[l:]) / d for l in range(1, k + 1)])
pf = lambda p: "< 0.0001" if p < 1e-4 else f"= {p:.3f}"
def lb(x, h):
    N = len(x); Q = N * (N + 2) * np.sum(acf(x, h) ** 2 / (N - np.arange(1, h + 1))); return Q, 1 - chi2.cdf(Q, h)
print("ACF of returns,         lags 1-3:", np.round(acf(r, 3), 3), " Ljung-Box p", pf(lb(r, 10)[1]))
print("ACF of squared returns, lags 1-3:", np.round(acf(r**2, 3), 3), " Ljung-Box p", pf(lb(r**2, 10)[1]))
def filt(p):
    o, a, b = p; v = np.empty(n); v[0] = r.var()
    for t in range(1, n): v[t] = o + a * r[t-1] ** 2 + b * v[t-1]
    return v
def nll(p):
    o, a, b = p
    if o <= 1e-6 or a < 0 or b < 0 or a + b >= 0.9999: return 1e10
    v = filt(p); return 0.5 * np.sum(np.log(v) + r ** 2 / v)
fit = minimize(nll, [0.1, 0.05, 0.8], method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 4000})
o, a, b = fit.x; v = filt(fit.x)
print(f"GARCH(1,1) estimates: omega {o:.3f} (0.05), alpha {a:.3f} (0.10), beta {b:.3f} (0.85); persistence {a+b:.3f}; long-run variance {o/(1-a-b):.2f}")
z = r / np.sqrt(v)
print("standardized residuals: ACF of squares lags 1-3:", np.round(acf(z**2, 3), 3), " Ljung-Box p", pf(lb(z**2, 10)[1]))
q = 2.326                                           # one-sided 99 percent normal quantile
var_g = q * np.sqrt(v); var_c = q * r.std()
print(f"1-day 99% VaR breaches (expected 1.0%): GARCH {np.mean(r < -var_g)*100:.1f}%, constant-volatility {np.mean(r < -var_c)*100:.1f}%")
calm = v < np.percentile(v, 25); wild = v > np.percentile(v, 75)
print(f"breach rate in calmest quarter of days: constant {np.mean(r[calm] < -var_c)*100:.1f}%, GARCH {np.mean(r[calm] < -var_g[calm])*100:.1f}%")
print(f"breach rate in wildest quarter of days: constant {np.mean(r[wild] < -var_c)*100:.1f}%, GARCH {np.mean(r[wild] < -var_g[wild])*100:.1f}%")
