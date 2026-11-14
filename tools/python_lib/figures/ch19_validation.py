import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import validation_curve
X, y = make_moons(600, noise=0.35, random_state=1)
depths = np.arange(1, 16)
tr, va = validation_curve(DecisionTreeClassifier(random_state=0), X, y, param_name="max_depth", param_range=depths, cv=5)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
for a, c, l in ((tr, B, "train"), (va, O, "validation (5-fold)")):
    ax.plot(depths, a.mean(1), color=c, lw=2.5, marker="o", label=l)
    ax.fill_between(depths, a.mean(1) - a.std(1), a.mean(1) + a.std(1), color=c, alpha=0.15)
b = depths[va.mean(1).argmax()]
ax.axvline(b, color="#333", ls="--"); ax.text(b + 0.2, 0.73, f"best depth {b}", fontsize=12)
ax.set_xlabel("max_depth"); ax.set_ylabel("accuracy"); ax.legend(fontsize=12)
plt.tight_layout(); plt.savefig("lib19_validation.png")
