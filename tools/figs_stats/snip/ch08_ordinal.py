import numpy as np
from scipy.optimize import minimize
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(82)
n = 1500
x = rng.normal(0, 1, n)
# proportional odds: logit P(y <= k) = theta_k - beta x, with theta = (-0.5, 1.2), beta = 0.9
th_true, beta_true = np.array([-0.5, 1.2]), 0.9
cum = 1 / (1 + np.exp(-(th_true[None, :] - beta_true * x[:, None])))
u = rng.random(n)
y = (u > cum[:, 0]).astype(int) + (u > cum[:, 1]).astype(int)       # 0 low, 1 mid, 2 high
print("class counts (low, mid, high):", np.bincount(y))
def nll(p):
    t1, d, b = p[0], np.exp(p[1]), p[2]; t2 = t1 + d
    c1 = 1 / (1 + np.exp(-(t1 - b * x))); c2 = 1 / (1 + np.exp(-(t2 - b * x)))
    pr = np.where(y == 0, c1, np.where(y == 1, c2 - c1, 1 - c2))
    return -np.log(np.clip(pr, 1e-12, None)).sum()
r = minimize(nll, [0, 0, 0], method="BFGS")
t1, t2, b = r.x[0], r.x[0] + np.exp(r.x[1]), r.x[2]
print(f"thresholds {t1:.2f}, {t2:.2f} (true -0.50, 1.20); beta {b:.2f} (true 0.90); OR per SD of x: {np.exp(b):.2f}")
c1 = 1/(1+np.exp(-(t1 - b*1.0))); c2 = 1/(1+np.exp(-(t2 - b*1.0)))
print(f"at x = +1 SD: P(low) {c1:.3f}  P(mid) {c2-c1:.3f}  P(high) {1-c2:.3f}")
# multinomial for comparison (unordered): 3 churn reasons from 2 features
rng = np.random.default_rng(83)
m = 1200; F = rng.normal(0, 1, (m, 2))
logits = np.column_stack([np.zeros(m), 0.8 * F[:, 0] - 0.2, -0.9 * F[:, 1] + 0.1])
P = np.exp(logits); P /= P.sum(1, keepdims=True)
cls = np.array([rng.choice(3, p=p) for p in P])
clf = LogisticRegression(C=1e6, max_iter=2000).fit(F, cls)
co = clf.coef_ - clf.coef_[0]           # relative to class 0 as the reference
print("multinomial coefficients vs reference class 0 (true: class1 [0.8, 0], class2 [0, -0.9]):")
print(np.round(co[1:], 2))
print("predicted probabilities at (1, 0):", np.round(clf.predict_proba([[1.0, 0.0]])[0], 3))
