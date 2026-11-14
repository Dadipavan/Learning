import numpy as np
from sklearn.datasets import make_friedman1
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as mse
X, y = make_friedman1(n_samples=1500, noise=2.0, random_state=0)
Xtr, Xtmp, ytr, ytmp = train_test_split(X, y, test_size=0.5, random_state=0)
Xva, Xte, yva, yte = train_test_split(Xtmp, ytmp, test_size=0.5, random_state=0)
m = GradientBoostingRegressor(n_estimators=600, learning_rate=0.1, max_depth=3, random_state=0).fit(Xtr, ytr)
tr = [mse(ytr, p) for p in m.staged_predict(Xtr)]
va = [mse(yva, p) for p in m.staged_predict(Xva)]
te = [mse(yte, p) for p in m.staged_predict(Xte)]
best = int(np.argmin(va)) + 1
print("best number of trees on validation:", best)
print("validation MSE at best %.3f, at 600 %.3f" % (va[best - 1], va[-1]))
print("test MSE at best %.3f, at 600 %.3f" % (te[best - 1], te[-1]))
print("train MSE at best %.3f, at 600 %.3f" % (tr[best - 1], tr[-1]))
# patience rule: stop when validation has not improved for 20 rounds
bestv, since = 1e9, 0
for i, v in enumerate(va, 1):
    if v < bestv - 1e-12: bestv, since, arg = v, 0, i
    else: since += 1
    if since == 20: print("patience 20 would stop at round %d and keep round %d" % (i, arg)); break
