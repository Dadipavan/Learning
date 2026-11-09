import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
X, _ = make_blobs(450, centers=4, cluster_std=1.1, random_state=3)
ks = range(2, 9)
sil = [silhouette_score(X, KMeans(k, n_init=10, random_state=0).fit_predict(X)) for k in ks]
inert = [KMeans(k, n_init=10, random_state=0).fit(X).inertia_ for k in ks]
fig, axs = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110)
lab = KMeans(4, n_init=10, random_state=0).fit(X)
cols = [B, O, T, P]
axs[0].scatter(X[:, 0], X[:, 1], c=[cols[i] for i in lab.labels_], s=10)
axs[0].scatter(*lab.cluster_centers_.T, marker="X", s=160, c="black"); axs[0].set_title("KMeans k=4")
axs[1].plot(list(ks), sil, color=B, marker="o", lw=2.5, label="silhouette")
axs[1].set_xlabel("k"); axs[1].set_ylabel("silhouette", color=B)
a2 = axs[1].twinx(); a2.plot(list(ks), inert, color=O, marker="s", lw=2.5); a2.set_ylabel("inertia", color=O); a2.spines["right"].set_visible(True)
axs[1].set_title("Choosing k")
plt.tight_layout(); plt.savefig("lib19_clusters.png")
