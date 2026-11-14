import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(31)
G, m = 30, 12                                    # 30 depots, 12 observations each
true_a = rng.normal(0, 20, G)                    # random intercept deviations (SD 20)
true_b = rng.normal(0, 3, G)                     # random slope deviations (SD 3)
vol = [rng.uniform(0, 10, m) for _ in range(G)]  # order volume
y = [200 + true_a[g] + (8 + true_b[g]) * vol[g] + rng.normal(0, 15, m) for g in range(G)]
def nll(p):
    b0, b1, l1, l2, z, ls = p
    s1, s2, sig2 = np.exp(l1), np.exp(l2), np.exp(2 * ls)
    r = np.tanh(z)
    D = np.array([[s1**2, r * s1 * s2], [r * s1 * s2, s2**2]])
    ll = 0
    for g in range(G):
        Z = np.column_stack([np.ones(m), vol[g]])
        V = Z @ D @ Z.T + sig2 * np.eye(m)
        res = y[g] - (b0 + b1 * vol[g])
        sign, logdet = np.linalg.slogdet(V)
        ll += -0.5 * (m * np.log(2 * np.pi) + logdet + res @ np.linalg.solve(V, res))
    return -ll
r = minimize(nll, [200, 8, np.log(15), np.log(2), 0.0, np.log(15)], method="Nelder-Mead",
             options={"maxiter": 4000, "xatol": 1e-4, "fatol": 1e-6})
b0, b1, l1, l2, z, ls = r.x
print("fixed intercept, slope :", round(b0, 1), round(b1, 2))
print("SD intercept, SD slope :", round(np.exp(l1), 1), round(np.exp(l2), 2), "(true 20 and 3)")
print("residual SD            :", round(np.exp(ls), 1), "(true 15)")
# shrunken (best linear unbiased) group lines vs separate OLS lines
s1, s2, sig2 = np.exp(l1), np.exp(l2), np.exp(2 * ls); rho = np.tanh(z)
D = np.array([[s1**2, rho * s1 * s2], [rho * s1 * s2, s2**2]])
raw, pooled = [], []
for g in range(G):
    Z = np.column_stack([np.ones(m), vol[g]])
    ols = np.linalg.lstsq(Z, y[g], rcond=None)[0]
    V = Z @ D @ Z.T + sig2 * np.eye(m)
    u = D @ Z.T @ np.linalg.solve(V, y[g] - Z @ np.array([b0, b1]))
    raw.append(ols[1]); pooled.append(b1 + u[1])
raw, pooled = np.array(raw), np.array(pooled)
true_slopes = 8 + true_b
print("slope RMSE, separate OLS lines :", round(np.sqrt(np.mean((raw - true_slopes) ** 2)), 2))
print("slope RMSE, partial pooling    :", round(np.sqrt(np.mean((pooled - true_slopes) ** 2)), 2))
print("spread of slopes: raw SD", round(raw.std(), 2), " shrunk SD", round(pooled.std(), 2))
