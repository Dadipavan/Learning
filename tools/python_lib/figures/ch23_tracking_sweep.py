import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
B, O, T, R = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26"
X, y = make_classification(n_samples=600, n_features=10, n_informative=4, flip_y=0.1, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
Cs = [0.001, 0.01, 0.1, 1, 10, 100]
tr, te = [], []
for C in Cs:
    m = LogisticRegression(C=C, max_iter=1000).fit(Xtr, ytr)
    tr.append(m.score(Xtr, ytr)); te.append(m.score(Xte, yte))
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.plot(Cs, tr, "o-", color=B, lw=2.5, ms=8, label="train accuracy")
ax.plot(Cs, te, "s-", color=O, lw=2.5, ms=8, label="test accuracy")
best = max(range(len(Cs)), key=lambda i: te[i])
ax.annotate(f"best run: C={Cs[best]}", (Cs[best], te[best]), xytext=(0.03, 0.687), fontsize=13,
            arrowprops=dict(arrowstyle="->", lw=2, color=R), color=R)
ax.set_xscale("log"); ax.set_xlabel("parameter C (one logged run per point)", fontsize=13)
ax.set_ylabel("accuracy", fontsize=13); ax.tick_params(labelsize=12); ax.legend(fontsize=12)
ax.set_title("What an experiment tracker lets you compare", fontsize=14)
fig.tight_layout(); fig.savefig("lib23_tracking_sweep.png")
