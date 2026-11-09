import numpy as np
rng = np.random.default_rng(21)
n = 40000
u = rng.normal(0, 1, n)                          # unobserved motivation
z = rng.random(n) < 0.5                          # random nudge (email) = instrument
take = (0.8 * z + 0.9 * u + rng.normal(0, 1, n)) > 0.7   # who actually uses the tool
y = 10 + 3.0 * take + 2.0 * u + rng.normal(0, 2, n)      # true effect of using the tool: +3
x = take.astype(float)
ols = np.polyfit(x, y, 1)[0]
# Wald / IV estimate = effect of nudge on outcome / effect of nudge on take-up
itt = y[z].mean() - y[~z].mean()
first = x[z].mean() - x[~z].mean()
print("OLS (confounded)  :", round(ols, 3))
print("nudge -> outcome  :", round(itt, 3))
print("nudge -> take-up  :", round(first, 3))
print("IV (Wald) estimate:", round(itt / first, 3))
# two-stage least squares done by hand, with the correct standard error
Z = np.column_stack([np.ones(n), z]); xhat = Z @ np.linalg.lstsq(Z, x, rcond=None)[0]
X2 = np.column_stack([np.ones(n), xhat]); b = np.linalg.lstsq(X2, y, rcond=None)[0]
Xr = np.column_stack([np.ones(n), x]); res = y - Xr @ b     # residuals use the REAL x
se = np.sqrt(res.var(ddof=2) * np.linalg.inv(X2.T @ X2)[1, 1])
print("2SLS estimate, SE :", round(b[1], 3), round(se, 3))
