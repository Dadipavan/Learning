import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

def exact_topk(base, Q, k):
    d = (Q ** 2).sum(1)[:, None] - 2 * Q @ base.T + (base ** 2).sum(1)[None, :]
    idx = np.argpartition(d, k, axis=1)[:, :k]
    order = np.take_along_axis(d, idx, 1).argsort(1)
    return np.take_along_axis(idx, order, 1)

def ivf_curve(X, nlist=64, k=10, probes=(1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64)):
    base, Q = X[:20000], X[20000:20200]
    truth = exact_topk(base, Q, k)
    km = KMeans(n_clusters=nlist, n_init=1, random_state=0).fit(base)
    lists = [np.where(km.labels_ == c)[0] for c in range(nlist)]
    cent = km.cluster_centers_.astype(np.float32)
    out = []
    for nprobe in probes:
        rec, scanned = 0.0, 0
        for q, t in zip(Q, truth):
            probe = np.argsort(((cent - q) ** 2).sum(1))[:nprobe]
            cand = np.concatenate([lists[c] for c in probe])
            best = cand[np.argsort(((base[cand] - q) ** 2).sum(1))[:k]]
            rec += len(set(best) & set(t)) / k
            scanned += len(cand)
        out.append((scanned / len(Q) / len(base), rec / len(Q)))
    return np.array(out)

blobs, _ = make_blobs(n_samples=20200, n_features=32, centers=40, cluster_std=6.0, random_state=0)
noise = np.random.default_rng(0).normal(size=(20200, 32))
a = ivf_curve(blobs.astype(np.float32)); b = ivf_curve(noise.astype(np.float32))
plt.rcParams.update({"font.size": 12})
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(a[:, 0], a[:, 1], "o-", color="#2b4fd6", lw=2.5, label="clustered data")
ax.plot(b[:, 0], b[:, 1], "s-", color="#b84a22", lw=2.5, label="Gaussian noise")
ax.plot([0, 1], [0, 1], "--", color="#777777", lw=1.5, label="random sample baseline")
ax.set_xlabel("share of vectors scanned"); ax.set_ylabel("recall@10"); ax.set_ylim(0, 1.05)
ax.legend(fontsize=11, loc="lower right"); ax.grid(alpha=0.25)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig("lib21_ivf_recall.png", dpi=110)
