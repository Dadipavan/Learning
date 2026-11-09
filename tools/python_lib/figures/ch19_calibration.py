import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
X, y = make_classification(20000, 20, n_informative=6, n_redundant=10, class_sep=0.8, flip_y=0.0, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, random_state=0)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.plot([0, 1], [0, 1], color="#999", ls="--", label="perfect")
for m, c, n in ((GaussianNB(), R, "Naive Bayes raw"), (CalibratedClassifierCV(GaussianNB(), method="isotonic", cv=5), T, "Naive Bayes + isotonic"), (LogisticRegression(max_iter=1000), B, "logistic")):
    p = m.fit(Xtr, ytr).predict_proba(Xte)[:, 1]
    fr, mp = calibration_curve(yte, p, n_bins=8)
    ax.plot(mp, fr, marker="o", color=c, lw=2.2, label=n)
ax.set_xlabel("mean predicted probability"); ax.set_ylabel("observed fraction positive"); ax.legend(fontsize=11)
plt.tight_layout(); plt.savefig("lib19_calibration.png")
