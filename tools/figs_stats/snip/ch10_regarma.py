import numpy as np
rng = np.random.default_rng(104)
n, rho, reps = 120, 0.7, 1000
def one():
    promo = np.zeros(n)
    for s in range(0, n, 10): promo[s:s+5] = 1                   # promo runs in 5-day blocks (also autocorrelated)
    e = rng.normal(0, 1, n); u = np.zeros(n)
    for t in range(1, n): u[t] = rho * u[t-1] + e[t]
    y = 50 + 3.0 * promo + u
    X = np.column_stack([np.ones(n), promo])
    b = np.linalg.solve(X.T @ X, X.T @ y); r = y - X @ b
    se_ols = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * (r @ r) / (n - 2))[1]
    # Cochrane-Orcutt: estimate rho from OLS residuals, transform, refit once more
    rh = np.dot(r[1:], r[:-1]) / np.dot(r[:-1], r[:-1])
    ys, Xs = y[1:] - rh * y[:-1], X[1:] - rh * X[:-1]
    bs = np.linalg.solve(Xs.T @ Xs, Xs.T @ ys); rs = ys - Xs @ bs
    se_co = np.sqrt(np.diag(np.linalg.inv(Xs.T @ Xs)) * (rs @ rs) / (n - 3))[1]
    return b[1], se_ols, bs[1], se_co
out = np.array([one() for _ in range(reps)])
print("promo effect (truth 3.0), 1000 simulated datasets")
print(f"OLS            : mean estimate {out[:,0].mean():.3f}, actual SD of estimates {out[:,0].std():.3f}, average reported SE {out[:,1].mean():.3f}, 95% CI coverage {np.mean(np.abs(out[:,0]-3) < 1.96*out[:,1]):.3f}")
print(f"AR(1) errors CO: mean estimate {out[:,2].mean():.3f}, actual SD of estimates {out[:,2].std():.3f}, average reported SE {out[:,3].mean():.3f}, 95% CI coverage {np.mean(np.abs(out[:,2]-3) < 1.96*out[:,3]):.3f}")
