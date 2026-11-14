import numpy as np
rng = np.random.default_rng(2024)
n = 5000                       # users per arm
def arm(effect):
    x = rng.gamma(4, 5, n)                     # pre-experiment spend (mean 20)
    y = 0.6 * x + rng.normal(0, 9, n) + effect  # experiment-period spend
    return x, y
xc, yc = arm(0.0)
xt, yt = arm(1.0)              # true lift: +1.0 per user
# naive difference in means
diff = yt.mean() - yc.mean()
se = np.sqrt(yt.var(ddof=1)/n + yc.var(ddof=1)/n)
# CUPED: theta from pooled data, then adjust each user
x = np.concatenate([xc, xt]); y = np.concatenate([yc, yt])
theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
adj = lambda xx, yy: yy - theta * (xx - x.mean())
ac, at = adj(xc, yc), adj(xt, yt)
diff2 = at.mean() - ac.mean()
se2 = np.sqrt(at.var(ddof=1)/n + ac.var(ddof=1)/n)
rho = np.corrcoef(x, y)[0, 1]
print("correlation rho  :", round(rho, 3))
print("theta            :", round(theta, 3))
print("naive lift, SE   :", round(diff, 3), round(se, 3))
print("CUPED lift, SE   :", round(diff2, 3), round(se2, 3))
print("variance ratio   :", round((se2/se)**2, 3), " 1 - rho^2 =", round(1 - rho**2, 3))
