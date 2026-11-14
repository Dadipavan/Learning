import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng(7)
N, D, Q = 5000, 256, 200
scale = 1.0 / np.sqrt(1 + np.arange(D) / 4.0)
centres = rng.normal(size=(100, D)) * scale
docs = centres[rng.integers(0, 100, N)] + 0.35 * rng.normal(size=(N, D)) * scale
queries = docs[rng.choice(N, Q, replace=False)] + 0.15 * rng.normal(size=(Q, D)) * scale
unit = lambda x: x / np.linalg.norm(x, axis=1, keepdims=True)
docs, queries = unit(docs), unit(queries)
top10 = lambda s: np.argsort(-s, axis=1)[:, :10]
truth = top10(queries @ docs.T)
rec = lambda f: np.mean([len(set(a) & set(b)) / 10 for a, b in zip(truth, f)])
ks = [256, 128, 64, 32]
r = [rec(top10(unit(queries[:, :k]) @ unit(docs[:, :k]).T)) for k in ks]
lo, hi = docs.min(), docs.max()
qi = lambda x: np.round((x - lo) / (hi - lo) * 255 - 128).astype(np.int8)
r8 = rec(top10(qi(queries).astype(np.int32) @ qi(docs).astype(np.int32).T))
bs = np.sign(queries) @ np.sign(docs).T
rb = rec(top10(bs))
hits = 0
for i in range(Q):
    cand = np.argsort(-bs[i])[:100]
    best = cand[np.argsort(-(docs[cand] @ queries[i]))[:10]]
    hits += len(set(best) & set(truth[i])) / 10
rr = hits / Q
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot([k * 4 for k in ks], r, "o-", color="#2b4fd6", lw=2, label="truncate + re-normalise (fp32)")
ax.plot([256], [r8], "s", color="#b84a22", ms=9, label="int8, all 256 dims")
ax.plot([32], [rb], "^", color="#aa2d26", ms=9, label="binary alone")
ax.plot([32], [rr], "D", color="#357a70", ms=9, label="binary + rescore 100")
ax.set_xscale("log", base=2); ax.set_xticks([32, 64, 128, 256, 512, 1024]); ax.set_xticklabels([32, 64, 128, 256, 512, 1024])
ax.set_xlabel("bytes per vector"); ax.set_ylabel("recall@10 vs full fp32"); ax.set_ylim(0, 1.05)
ax.set_title("Compression trades bytes for recall (synthetic data)")
ax.legend(frameon=False, loc="lower right"); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch02_compression.png", dpi=110)
print(r, r8, rb, rr)
