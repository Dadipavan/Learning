import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import average_precision_score, recall_score, precision_score
X, y = make_classification(4000, 8, n_informative=4, weights=[0.97], flip_y=0.01, class_sep=1.0, random_state=1)
Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, random_state=0)
def smote(Xp, n_new, k=5, seed=0):
    r = np.random.default_rng(seed); nn = NearestNeighbors(n_neighbors=k + 1).fit(Xp)
    idx = nn.kneighbors(Xp, return_distance=False)[:, 1:]
    i = r.integers(0, len(Xp), n_new); j = idx[i, r.integers(0, k, n_new)]
    return Xp[i] + r.random((n_new, 1)) * (Xp[j] - Xp[i])
def fit_eval(Xa, ya, tag):
    m = RandomForestClassifier(200, random_state=0, n_jobs=-1).fit(Xa, ya); p = m.predict_proba(Xte)[:, 1]
    print(f"{tag:22s} PR-AUC {average_precision_score(yte, p):.3f}  @0.5: recall {recall_score(yte, p>.5):.2f} prec {precision_score(yte, p>.5):.2f}")
print("train positives", ytr.sum(), "of", len(ytr))
fit_eval(Xtr, ytr, "baseline")
Xp = Xtr[ytr == 1]; new = smote(Xp, (ytr == 0).sum() - len(Xp))
fit_eval(np.r_[Xtr, new], np.r_[ytr, np.ones(len(new), int)], "SMOTE to 50/50")
m = RandomForestClassifier(200, random_state=0, class_weight="balanced_subsample", n_jobs=-1).fit(Xtr, ytr); p = m.predict_proba(Xte)[:, 1]
print(f"{'class_weight':22s} PR-AUC {average_precision_score(yte, p):.3f}  @0.5: recall {recall_score(yte, p>.5):.2f} prec {precision_score(yte, p>.5):.2f}")
# the leakage mistake: SMOTE before the split -> CV score inflated
from sklearn.model_selection import cross_val_score, StratifiedKFold
Xp = X[y == 1]; new = smote(Xp, (y == 0).sum() - len(Xp)); Xa = np.r_[X, new]; ya = np.r_[y, np.ones(len(new), int)]
s = cross_val_score(RandomForestClassifier(100, random_state=0, n_jobs=-1), Xa, ya, cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="average_precision")
print("WRONG (SMOTE before CV) PR-AUC", s.mean().round(3))
