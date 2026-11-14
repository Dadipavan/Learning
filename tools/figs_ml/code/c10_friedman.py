import warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy import stats
from sklearn.datasets import load_iris, load_wine, load_breast_cancer, load_digits, make_classification, make_moons, make_circles
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
data = {"iris": load_iris(return_X_y=True), "wine": load_wine(return_X_y=True), "cancer": load_breast_cancer(return_X_y=True),
        "digits": load_digits(return_X_y=True), "moons": make_moons(600, noise=0.3, random_state=0),
        "circles": make_circles(600, noise=0.15, factor=0.5, random_state=0)}
for s in range(6):
    data["synth%d" % s] = make_classification(600, 12, n_informative=4 + s % 3, n_redundant=2, flip_y=0.05, class_sep=0.8, random_state=s)
models = {"logreg": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
          "forest": RandomForestClassifier(100, random_state=0),
          "knn": make_pipeline(StandardScaler(), KNeighborsClassifier(15))}
cv = StratifiedKFold(5, shuffle=True, random_state=0)
names = list(data); S = np.array([[cross_val_score(m, *data[d], cv=cv).mean() for m in models.values()] for d in names])
print("%-9s" % "dataset", *["%7s" % k for k in models])
for d, row in zip(names, S): print("%-9s" % d, *["%7.3f" % v for v in row])
ranks = np.array([stats.rankdata(-row) for row in S]); R = ranks.mean(0)
print("mean rank (1 = best):", dict(zip(models, R.round(2))))
fr = stats.friedmanchisquare(*S.T); print("Friedman chi2 = %.2f, p = %.4f (N = %d datasets, k = 3 models)" % (fr.statistic, fr.pvalue, len(names)))
N, k = len(names), 3; cd = 2.343 * np.sqrt(k * (k + 1) / (6 * N))
print("Nemenyi critical difference (alpha 0.05, q = 2.343): %.2f" % cd)
print("rank gaps: logreg-forest %.2f, knn-forest %.2f, logreg-knn %.2f" % (R[0] - R[1], R[2] - R[1], R[0] - R[2]))
for a, b in [(0, 1), (1, 2), (0, 2)]:
    w = stats.wilcoxon(S[:, a], S[:, b]); print("Wilcoxon %s vs %s: W = %.0f, p = %.4f, median diff %.4f" % (list(models)[a], list(models)[b], w.statistic, w.pvalue, np.median(S[:, a] - S[:, b])))
