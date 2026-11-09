import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2
rng = np.random.default_rng(23)
n = 800
x = (rng.random(n) < 0.5).astype(float)             # a promotion shown at sign-up
def simulate(fading):
    t = np.empty(n)
    for i in range(n):
        h1 = 0.08 * np.exp(-0.7 * x[i])             # promotion cuts the hazard by half ...
        if not fading:
            t[i] = rng.exponential(1 / h1)
        else:
            t1 = rng.exponential(1 / h1)            # ... but only for months 0-3
            t[i] = t1 if t1 < 3 else 3 + rng.exponential(1 / 0.08)
    c = rng.uniform(10, 40, n)
    return np.minimum(t, c), (t <= c).astype(int)
def ph_test(time, event, x):
    """Does the effect of x change with log(time)? Likelihood-ratio test of x*log(t) in a Cox model."""
    o = np.argsort(time); time, event, x = time[o], event[o], x[o]
    n1 = np.cumsum(x[::-1])[::-1]; n0 = np.cumsum((1 - x)[::-1])[::-1]   # risk-set counts, no ties
    ev = event == 1; g = np.log(time[ev])
    def nll(p, with_trend=True):
        theta = p[0] + (p[1] * g if with_trend else 0)
        return -(x[ev] * theta - np.log(n0[ev] + n1[ev] * np.exp(theta))).sum()
    r0 = minimize(lambda p: nll([p[0]], False), [0.0])
    r1 = minimize(nll, [0.0, 0.0])
    lr = 2 * (r0.fun - r1.fun)
    return np.exp(r0.x[0]), r1.x[1], lr, chi2.sf(lr, 1)
for fading in (False, True):
    time, event = simulate(fading)
    hr, slope, lr, p = ph_test(time, event, x)
    print("effect fades after month 3:" if fading else "constant effect (PH holds):",
          f"HR {hr:.2f}  log-HR change per unit log-time {slope:+.2f}  LR {lr:.2f}  p {p:.4f}")
