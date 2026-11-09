import numpy as np
from sklearn.cluster import DBSCAN, HDBSCAN
from sklearn.datasets import make_blobs
from sklearn.metrics import adjusted_rand_score
rng = np.random.default_rng(0)
X1, y1 = make_blobs(n_samples=[200, 200], centers=[[0, 0], [6, 0]], cluster_std=[0.3, 1.5], random_state=0)
X2 = rng.uniform(-3, 9, (40, 2)); X = np.r_[X1, X2]; y = np.r_[y1, -np.ones(40, int)]
for eps in (0.3, 0.6, 1.0):
    lab = DBSCAN(eps=eps, min_samples=10).fit_predict(X)
    print("DBSCAN eps", eps, "clusters", len(set(lab) - {-1}), "noise", (lab == -1).sum())
h = HDBSCAN(min_cluster_size=30, copy=True).fit(X)
print("HDBSCAN clusters", len(set(h.labels_) - {-1}), "noise", (h.labels_ == -1).sum(),
      "ARI on non-noise truth", round(adjusted_rand_score(y[y >= 0], h.labels_[y >= 0]), 3))
