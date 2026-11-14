import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(13)
T0, T1, J = 24, 12, 8                        # months before / after launch, donor regions
f = np.cumsum(rng.normal(0, 1, T0 + T1)) + 0.3 * np.arange(T0 + T1)   # a shared trend
load = rng.uniform(0.5, 1.5, J + 1)
Y = load[:, None] * f + rng.normal(0, 0.3, (J + 1, T0 + T1)) + 10 * rng.uniform(0.5, 1.5, (J + 1, 1))
Y[0] = 0.6 * Y[3] + 0.4 * Y[6] + rng.normal(0, 0.3, T0 + T1)   # region 0 resembles a mix of donors
Y[0, T0:] -= 4.0                             # region 0 launches a change at month 24: true effect -4
treated, donors = Y[0], Y[1:]
def loss(w): return np.sum((treated[:T0] - w @ donors[:, :T0]) ** 2)
cons = ({"type": "eq", "fun": lambda w: w.sum() - 1},)
res = minimize(loss, np.ones(J) / J, bounds=[(0, 1)] * J, constraints=cons, method="SLSQP")
w = res.x
synth = w @ donors
gap = treated - synth
print("weights:", np.round(w, 2))
print("pre-launch RMSE of fit :", round(np.sqrt(np.mean(gap[:T0] ** 2)), 2))
print("mean post gap (effect) :", round(gap[T0:].mean(), 2))
# placebo test: pretend each donor was treated, compute its post/pre RMSE ratio
def ratio(i):
    others = np.delete(Y, i, axis=0); tr = Y[i]
    r = minimize(lambda w: np.sum((tr[:T0] - w @ others[:, :T0]) ** 2), np.ones(J) / J, bounds=[(0, 1)] * J,
                 constraints=cons, method="SLSQP")
    g = tr - r.x @ others
    return np.sqrt(np.mean(g[T0:] ** 2)) / np.sqrt(np.mean(g[:T0] ** 2))
ratios = np.array([ratio(i) for i in range(J + 1)])
print("post/pre RMSE ratios (region 0 first):", np.round(ratios, 1))
print("rank of region 0:", int((ratios >= ratios[0]).sum()), "of", J + 1)
