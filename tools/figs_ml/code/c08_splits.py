import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold, GroupKFold, TimeSeriesSplit
n = 12; g = np.repeat(np.arange(4), 3); y = np.array([0,0,0,0,1,0,0,0,1,0,0,1])
for name, sp, kw in [("KFold", KFold(3), {}), ("GroupKFold", GroupKFold(3), {"groups": g}), ("TimeSeriesSplit", TimeSeriesSplit(3), {})]:
    print(name)
    for i, (a, b) in enumerate(sp.split(np.zeros(n), y, **kw)): print("  fold", i, "train", a.tolist(), "test", b.tolist())
