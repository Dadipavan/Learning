import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
X, y = make_moons(300, noise=0.3, random_state=0)
models = [("Logistic", LogisticRegression()), ("Tree depth 20", DecisionTreeClassifier(random_state=0)),
          ("Forest", RandomForestClassifier(100, random_state=0)), ("SVM rbf", SVC()),
          ("kNN k=15", KNeighborsClassifier(15)), ("Naive Bayes", GaussianNB())]
xx, yy = np.meshgrid(np.linspace(-2, 3, 200), np.linspace(-1.6, 2.2, 200))
fig, axs = plt.subplots(2, 3, figsize=(8, 5.2), dpi=110)
for ax, (n, m) in zip(axs.ravel(), models):
    m.fit(X, y); z = m.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, z, levels=[-.5, .5, 1.5], colors=[B, O], alpha=0.25)
    ax.scatter(X[:, 0], X[:, 1], c=np.where(y == 0, B, O), s=8)
    ax.set_title(n, fontsize=12); ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.savefig("lib19_boundaries.png")
