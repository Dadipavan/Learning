import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, n_features=10, n_informative=4, random_state=7)
def score(depth, seed):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=seed)
    return RandomForestClassifier(n_estimators=20, max_depth=depth, random_state=seed).fit(Xtr, ytr).score(Xte, yte)
seeds = list(range(10))
a = np.array([score(4, s) for s in seeds]); b = np.array([score(6, s) for s in seeds])
fig, ax = plt.subplots(figsize=(8, 4.2))
for s in seeds:
    ax.plot([0, 1], [a[s], b[s]], color="#bbbbbb", lw=1, zorder=1)
ax.scatter(np.zeros(10), a, color="#2b4fd6", s=40, zorder=3, label="model A (depth 4)")
ax.scatter(np.ones(10), b, color="#b84a22", s=40, zorder=3, label="model B (depth 6)")
for x, v, c in [(0, a, "#2b4fd6"), (1, b, "#b84a22")]:
    ax.hlines(v.mean(), x - .18, x + .18, color=c, lw=3, zorder=4)
    ax.fill_between([x - .18, x + .18], v.mean() - v.std(ddof=1), v.mean() + v.std(ddof=1), color=c, alpha=.15)
ax.set_xticks([0, 1]); ax.set_xticklabels(["A", "B"]); ax.set_xlim(-.5, 1.5)
ax.set_ylabel("Test accuracy"); ax.grid(alpha=.25, axis="y")
ax.set_title(f"Same data, 10 seeds: mean A {a.mean():.3f}, B {b.mean():.3f}; spread (1 std) {a.std(ddof=1):.3f}, {b.std(ddof=1):.3f}")
ax.legend(loc="lower right")
fig.tight_layout(); fig.savefig("ch02d_seed_noise.png", dpi=110)
