import numpy as np
rng = np.random.default_rng(8)
n = 300
treat = rng.integers(0, 2, n)
days = np.where(treat == 1, rng.uniform(5, 25, n), rng.uniform(20, 60, n))   # treated sites watched for fewer days
rate = np.exp(-1.2 + 0.4 * treat)                                             # true events per day
y = rng.poisson(rate * days)

def poisson_irls(X, y, offset, iters=25):
    b = np.zeros(X.shape[1]); b[0] = np.log(y.mean() + 0.1)
    for _ in range(iters):
        eta = X @ b + offset; mu = np.exp(eta)
        W = mu; z = eta - offset + (y - mu) / mu
        XtW = X.T * W
        b = np.linalg.solve(XtW @ X, XtW @ z)
    mu = np.exp(X @ b + offset)
    se = np.sqrt(np.diag(np.linalg.inv((X.T * mu) @ X)))
    return b, se
X = np.column_stack([np.ones(n), treat])
b0, s0 = poisson_irls(X, y, np.zeros(n))
b1, s1 = poisson_irls(X, y, np.log(days))
print("true treatment effect on log rate: 0.400")
print(f"no offset : coef {b0[1]:.3f} (SE {s0[1]:.3f})  rate ratio {np.exp(b0[1]):.2f}")
print(f"offset    : coef {b1[1]:.3f} (SE {s1[1]:.3f})  rate ratio {np.exp(b1[1]):.2f}")
print(f"mean days: control {days[treat==0].mean():.1f}, treated {days[treat==1].mean():.1f}")
print(f"baseline rate per day (offset model): {np.exp(b1[0]):.3f}  (true {np.exp(-1.2):.3f})")
