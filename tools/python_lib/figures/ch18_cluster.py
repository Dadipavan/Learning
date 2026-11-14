import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from scipy.cluster import vq
from scipy.spatial import KDTree
rng = np.random.default_rng(4)
pts = np.vstack([rng.normal(c, 0.6, (60, 2)) for c in ([0, 0], [4, 1], [2, 4.5])])
cent, lab = vq.kmeans2(pts, 3, seed=1, minit="++")
q = np.array([2.0, 2.0])
tree = KDTree(pts); d, idx = tree.query(q, k=5)
cols = [B, O, T]
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
for k in range(3): ax.scatter(*pts[lab == k].T, s=18, color=cols[k], alpha=0.7)
ax.scatter(*cent.T, marker="X", s=200, color="black", label="k-means centres")
ax.scatter(*pts[idx].T, s=90, facecolors="none", edgecolors=R, linewidths=2, label="5 nearest to query")
ax.scatter(*q, marker="*", s=250, color=P, label="query point")
ax.set_xlabel("feature 1"); ax.set_ylabel("feature 2"); ax.legend(frameon=False, fontsize=11)
ax.set_title("KDTree neighbours and k-means clusters")
fig.tight_layout(); fig.savefig("lib18_cluster.png")
