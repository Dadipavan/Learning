import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd, os, tempfile, tracemalloc
BL, OR, TE, RE, PU = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 13, "axes.titlesize": 15})

rng = np.random.default_rng(7); n, nk, npart = 1_000_000, 1000, 8
w = 1 / np.arange(1, nk + 1); keys = rng.choice(nk, n, p=w / w.sum()); salt = rng.integers(0, 8, n)
sz = lambda k: np.bincount(pd.util.hash_array(k.astype(np.int64)) % npart, minlength=npart)
a, b = sz(keys), sz(keys * 8 + salt); x = np.arange(npart); wd = 0.38
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.bar(x - wd / 2, a / 1e3, wd, color=RE, label="by key (max/mean %.2f)" % (a.max() / a.mean()))
ax.bar(x + wd / 2, b / 1e3, wd, color=TE, label="by key + salt (max/mean %.2f)" % (b.max() / b.mean()))
ax.axhline(n / npart / 1e3, color="#333", ls=":", lw=2); ax.text(7.4, n / npart / 1e3 + 4, "ideal", ha="right")
ax.set_xlabel("partition"); ax.set_ylabel("rows (thousands)"); ax.set_title("Skew: one hot key overloads one partition"); ax.legend()
fig.tight_layout(); fig.savefig("lib22_skew.png", dpi=110)
