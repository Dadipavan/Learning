import numpy as np
rng = np.random.default_rng(17)
n = 600
annual = (rng.random(n) < 0.4).astype(float)       # 1 = annual plan
tickets = rng.poisson(1.5, n).astype(float)         # support tickets in first month
# true model: hazard = 0.05 * exp(-0.7 * annual + 0.25 * tickets)
rate = 0.05 * np.exp(-0.7 * annual + 0.25 * tickets)
t_event = rng.exponential(1 / rate)
t_cens = rng.uniform(6, 36, n)                      # administrative / random censoring
time = np.minimum(t_event, t_cens); event = (t_event <= t_cens).astype(int)
X = np.column_stack([annual, tickets])
order = np.argsort(time); time, event, X = time[order], event[order], X[order]
def fit_cox(X, time, event, iters=25):
    beta = np.zeros(X.shape[1])
    for _ in range(iters):
        eta = np.exp(X @ beta)
        # risk-set sums via reverse cumulative sums (data sorted by time, no ties)
        S0 = np.cumsum(eta[::-1])[::-1]
        S1 = np.cumsum((eta[:, None] * X)[::-1], axis=0)[::-1]
        S2 = np.cumsum((eta[:, None, None] * X[:, :, None] * X[:, None, :])[::-1], axis=0)[::-1]
        ev = event == 1
        grad = (X[ev] - S1[ev] / S0[ev, None]).sum(axis=0)
        mean = S1[ev] / S0[ev, None]
        hess = (S2[ev] / S0[ev, None, None] - mean[:, :, None] * mean[:, None, :]).sum(axis=0)
        beta = beta + np.linalg.solve(hess, grad)
    return beta, np.sqrt(np.diag(np.linalg.inv(hess)))
beta, se = fit_cox(X, time, event)
print("events:", event.sum(), "of", n)
for name, b, s, tb in zip(["annual", "tickets"], beta, se, [-0.7, 0.25]):
    print(f"{name:8s} beta {b:6.3f} SE {s:5.3f} HR {np.exp(b):5.3f} 95% CI ({np.exp(b-1.96*s):.3f}, {np.exp(b+1.96*s):.3f})  true beta {tb}")
