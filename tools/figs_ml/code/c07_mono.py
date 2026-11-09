import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
rng = np.random.default_rng(0)
x = rng.uniform(0, 10, 400); y = 0.5 * x + rng.normal(0, 1.5, 400)
grid = np.linspace(0, 10, 400).reshape(-1, 1)
for cst in (None, [1]):
    m = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.1, monotonic_cst=cst, random_state=0).fit(x.reshape(-1, 1), y)
    p = m.predict(grid)
    print("monotonic_cst =", cst, "downward steps on grid:", int((np.diff(p) < -1e-12).sum()), " total drop %.2f" % abs(np.diff(p)[np.diff(p) < 0].sum()))
