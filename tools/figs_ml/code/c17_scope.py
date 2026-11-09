import numpy as np, pandas as pd
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import average_precision_score
X, y = make_classification(3000, 10, n_informative=5, weights=[0.9], random_state=0)
cv = StratifiedKFold(5, shuffle=True, random_state=0); log = []
for name, m in [("prior (dummy)", DummyClassifier(strategy="prior")), ("logistic", LogisticRegression(max_iter=1000)), ("hist-GB", HistGradientBoostingClassifier(random_state=0))]:
    p = cross_val_predict(m, X, y, cv=cv, method="predict_proba")[:, 1]
    log.append({"id": len(log) + 1, "model": name, "PR-AUC": round(average_precision_score(y, p), 3)})
df = pd.DataFrame(log); df["lift_vs_baseline"] = (df["PR-AUC"] / df["PR-AUC"][0]).round(2)
print(df.to_string(index=False))
