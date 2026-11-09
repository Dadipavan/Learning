import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
rng = np.random.default_rng(0)
C = np.array([[1, 0.9], [0.9, 1]]); Xn = rng.multivariate_normal([0, 0], C, 600)
Xa = np.array([[2.0, -2.0], [-1.5, 1.8], [3.2, 3.2]])        # two contextual, one extreme
iso = IsolationForest(n_estimators=300, random_state=0).fit(Xn)
lof = LocalOutlierFactor(n_neighbors=30, novelty=True).fit(Xn)
si, sl = -iso.score_samples(Xn), -lof.score_samples(Xn)
print("99th percentile of normal scores: IF %.3f  LOF %.2f" % (np.percentile(si, 99), np.percentile(sl, 99)))
for p, a, b in zip(Xa, -iso.score_samples(Xa), -lof.score_samples(Xa)):
    print("point %-12s IF %.3f  LOF %.2f   above the 99th percentile: IF %s, LOF %s" % (p, a, b, a > np.percentile(si, 99), b > np.percentile(sl, 99)))
