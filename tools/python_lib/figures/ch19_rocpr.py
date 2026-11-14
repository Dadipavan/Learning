import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score, average_precision_score
X, y = make_classification(6000, 15, n_informative=5, weights=[0.97], flip_y=0.02, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, random_state=0)
fig, axs = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110)
for m, c, n in ((LogisticRegression(max_iter=1000), B, "logistic"), (RandomForestClassifier(200, random_state=0), O, "forest")):
    p = m.fit(Xtr, ytr).predict_proba(Xte)[:, 1]
    f, t, _ = roc_curve(yte, p); axs[0].plot(f, t, color=c, lw=2.5, label=f"{n} AUC {roc_auc_score(yte, p):.2f}")
    pr, rc, _ = precision_recall_curve(yte, p); axs[1].plot(rc, pr, color=c, lw=2.5, label=f"{n} AP {average_precision_score(yte, p):.2f}")
axs[0].plot([0, 1], [0, 1], color="#999", ls="--"); axs[1].axhline(yte.mean(), color="#999", ls="--")
axs[0].set_xlabel("false positive rate"); axs[0].set_ylabel("true positive rate"); axs[0].set_title("ROC")
axs[1].set_xlabel("recall"); axs[1].set_ylabel("precision"); axs[1].set_title("Precision-recall")
for a in axs: a.legend(fontsize=10)
plt.tight_layout(); plt.savefig("lib19_rocpr.png")
