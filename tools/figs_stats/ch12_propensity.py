import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, Rd, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
rng = np.random.default_rng(42)
n = 20000
age = rng.normal(35, 8, n); tenure = rng.exponential(12, n); activity = rng.normal(0, 1, n)
logit = -1.0 + 0.9 * activity + 0.04 * (tenure - 12) + 0.02 * (age - 35)
t = rng.random(n) < 1 / (1 + np.exp(-logit))
X = np.column_stack([age, tenure, activity]); Z = (X - X.mean(0)) / X.std(0)
ps = LogisticRegression(C=1e6, max_iter=1000).fit(Z, t).predict_proba(Z)[:, 1]
w = np.where(t, t.mean() / ps, (1 - t.mean()) / (1 - ps))
def smd(a, b, wa, wb):
    ma, mb = np.average(a, weights=wa), np.average(b, weights=wb)
    va, vb = np.average((a-ma)**2, weights=wa), np.average((b-mb)**2, weights=wb)
    return (ma - mb) / np.sqrt((va + vb) / 2)
names = ["age", "tenure", "activity"]
raw = [smd(X[t, j], X[~t, j], None if False else np.ones(t.sum()), np.ones((~t).sum())) for j in range(3)]
wtd = [smd(X[t, j], X[~t, j], w[t], w[~t]) for j in range(3)]
fig, ax = plt.subplots(1, 2, figsize=(9, 4.2))
bins = np.linspace(0, 1, 41)
ax[0].hist(ps[~t], bins, alpha=.6, color=B, label="not treated"); ax[0].hist(ps[t], bins, alpha=.6, color=O, label="treated")
ax[0].set_xlabel("propensity score"); ax[0].set_yticks([]); ax[0].set_title("Overlap: both groups cover the range"); ax[0].legend(frameon=False)
y = np.arange(3)
ax[1].scatter(np.abs(raw), y, color=Rd, s=60, label="before weighting", zorder=3)
ax[1].scatter(np.abs(wtd), y, color=T, s=60, marker="s", label="after IPW", zorder=3)
ax[1].axvline(0.1, color="k", ls="--", lw=1); ax[1].text(0.105, 2.35, "0.1 rule of thumb", fontsize=9)
ax[1].set_yticks(y); ax[1].set_yticklabels(names); ax[1].set_xlabel("absolute standardized mean difference")
ax[1].set_title("Balance (love plot)"); ax[1].legend(frameon=False, loc="center right", fontsize=9)
plt.tight_layout(); plt.savefig("ch12_propensity.png", dpi=110)
