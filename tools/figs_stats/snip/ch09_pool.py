import numpy as np
from scipy.optimize import minimize
from scipy.special import betaln
n = np.array([20, 35, 50, 80, 120, 200, 400, 800])
rng = np.random.default_rng(92)
true_p = rng.beta(4, 28, 8)                  # stores vary around 12.5 percent
k = rng.binomial(n, true_p)
raw = k / n
def nll(t):
    a, b = np.exp(t)
    return -(betaln(k + a, n - k + b) - betaln(a, b)).sum()     # beta-binomial marginal likelihood (constants dropped)
r = minimize(nll, [np.log(10), np.log(80)], method="Nelder-Mead")
a, b = np.exp(r.x)
pooled = k.sum() / n.sum()
partial = (k + a) / (n + a + b)
print(f"fitted population prior: Beta({a:.1f}, {b:.1f}), mean {a/(a+b):.3f}, equivalent prior sample size {a+b:.0f}")
print(f"complete pooling rate: {pooled:.3f}")
print("store   n     k   no pooling   partial pooling   weight on own data   true p")
for i in range(8):
    w = n[i] / (n[i] + a + b)
    print(f"{i+1:>5} {n[i]:>4} {k[i]:>5}   {raw[i]:10.3f}   {partial[i]:15.3f}   {w:18.2f}   {true_p[i]:6.3f}")
print("squared error vs truth: no pooling", round(((raw - true_p)**2).sum(), 5), " partial", round(((partial - true_p)**2).sum(), 5), " complete", round(((pooled - true_p)**2).sum(), 5))
