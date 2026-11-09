import numpy as np
rng = np.random.default_rng(8)
n = 6000
score = rng.uniform(0, 100, n)                   # running variable; cutoff at 50 gets a coaching programme
treated = score >= 50
y = 30 + 0.4 * score + 5.0 * treated + rng.normal(0, 6, n)   # true jump = 5
print("naive treated - untreated:", round(y[treated].mean() - y[~treated].mean(), 2))
def local_linear(h):
    m = np.abs(score - 50) <= h
    x = score[m] - 50
    X = np.column_stack([np.ones(m.sum()), treated[m], x, x * treated[m]])
    b = np.linalg.lstsq(X, y[m], rcond=None)[0]
    res = y[m] - X @ b
    se = np.sqrt(res.var(ddof=4) * np.linalg.inv(X.T @ X)[1, 1])
    return b[1], se, m.sum()
for h in (5, 10, 20, 50):
    b, se, k = local_linear(h)
    print(f"bandwidth {h:2d}: jump {b:6.2f}  SE {se:4.2f}  n {k}")
