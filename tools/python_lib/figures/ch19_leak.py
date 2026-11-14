import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
rng = np.random.RandomState(0)
leak, ok = [], []
for s in range(30):
    r = np.random.RandomState(s)
    X = r.normal(size=(60, 2000)); y = r.randint(0, 2, 60)
    Xs = SelectKBest(f_classif, k=20).fit_transform(X, y)
    leak.append(cross_val_score(LogisticRegression(), Xs, y, cv=5).mean())
    p = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression())
    ok.append(cross_val_score(p, X, y, cv=5).mean())
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.hist(leak, bins=10, color=R, alpha=0.8, label="select on all rows, then CV (leak)")
ax.hist(ok, bins=10, color=B, alpha=0.8, label="selection inside Pipeline")
ax.axvline(0.5, color="#333", ls="--", label="chance (0.5)")
ax.set_xlabel("5-fold CV accuracy on pure noise (30 datasets)"); ax.set_ylabel("count")
ax.set_ylim(0, 11); ax.legend(fontsize=11, loc="upper center"); plt.tight_layout(); plt.savefig("lib19_leak.png")
