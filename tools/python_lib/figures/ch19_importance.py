import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
X, y = make_regression(1500, 6, n_informative=3, noise=15, random_state=0, shuffle=False)
names = [f"f{i}" for i in range(6)]
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
m = RandomForestRegressor(150, random_state=0, n_jobs=1).fit(Xtr, ytr)
pi = permutation_importance(m, Xte, yte, n_repeats=15, random_state=0)
fig, axs = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110)
o = np.argsort(pi.importances_mean)
axs[0].barh(np.array(names)[o], pi.importances_mean[o], xerr=pi.importances_std[o], color=B)
axs[0].set_xlabel("drop in R2 when shuffled"); axs[0].set_title("Permutation importance")
PartialDependenceDisplay.from_estimator(m, Xte, [0], ax=axs[1], line_kw={"color": O, "lw": 2.5})
axs[1].set_title("Partial dependence of f0")
plt.tight_layout(); plt.savefig("lib19_importance.png")
