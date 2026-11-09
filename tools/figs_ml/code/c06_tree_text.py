import numpy as np
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text
X, y = load_iris(return_X_y=True); X = X[:, 2:]
t = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y)
print(export_text(t, feature_names=["petal_len", "petal_wid"], show_weights=True))
print("train acc", round(t.score(X, y),3), "leaves", t.get_n_leaves())
from sklearn.tree import DecisionTreeClassifier as D
for d in (1, 2, 3, 8): print("depth", d, "leaves", D(max_depth=d, random_state=0).fit(X, y).get_n_leaves(), "acc", D(max_depth=d, random_state=0).fit(X, y).score(X, y))
