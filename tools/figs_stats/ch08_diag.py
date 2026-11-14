import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
B, O, T = "#2b4fd6", "#b84a22", "#357a70"
rng = np.random.default_rng(84)
n = 2000
X = rng.normal(0, 1, (n, 2))
p = 1 / (1 + np.exp(-(-1.0 + 1.1 * X[:, 0] + 0.6 * X[:, 1])))
y = (rng.random(n) < p).astype(int)
tr, te = slice(0, 1200), slice(1200, n)
m = LogisticRegression(C=1e6).fit(X[tr], y[tr])
ph = m.predict_proba(X[te])[:, 1]; yt = y[te]
o = np.argsort(-ph); ys = yt[o]
tpr = np.r_[0, np.cumsum(ys) / ys.sum()]; fpr = np.r_[0, np.cumsum(1 - ys) / (1 - ys).sum()]
fig, ax = plt.subplots(1, 2, figsize=(10, 4.3))
ax[0].plot(fpr, tpr, color=B, lw=2.5); ax[0].plot([0, 1], [0, 1], color="#999", ls="--")
ax[0].set_xlabel("false positive rate"); ax[0].set_ylabel("true positive rate"); ax[0].set_title("ROC curve (test AUC 0.784)")
groups = np.array_split(np.argsort(ph), 10)
mp = [ph[g].mean() for g in groups]; ob = [yt[g].mean() for g in groups]
ax[1].plot([0, 1], [0, 1], color="#999", ls="--", label="perfect calibration")
ax[1].plot(mp, ob, color=O, marker="o", lw=2, label="test deciles")
ax[1].set_xlabel("mean predicted probability"); ax[1].set_ylabel("observed rate"); ax[1].set_title("Calibration by decile"); ax[1].legend(frameon=False)
plt.tight_layout(); plt.savefig("ch08_diag.png", dpi=110)
