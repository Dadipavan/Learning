import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BL, OR, TE, RD, PU = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

import numpy as np

labels = list("ABCDEFGHIJKL")
edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 0), (3, 2), (3, 4), (4, 2), (4, 5), (5, 4), (5, 6),
         (6, 2), (6, 7), (7, 8), (8, 9), (9, 7), (9, 10), (10, 2), (10, 11), (8, 2)]   # L (11) has no out-links
n = 12
A = np.zeros((n, n))
for i, j in edges:
    A[j, i] = 1                                     # column i = where page i links to
out_deg = A.sum(axis=0)
P = np.where(out_deg > 0, A / np.where(out_deg == 0, 1, out_deg), 1 / n)   # dangling column -> uniform

def pr(d):
    G = d * P + (1 - d) / n * np.ones((n, n)); x = np.ones(n) / n
    for _ in range(2000): x = G @ x
    return x
fig, ax = plt.subplots(1, 2, figsize=(10, 4.4), gridspec_kw={"width_ratios": [1, 1.2]})
ang = np.linspace(0, 2 * np.pi, n, endpoint=False) + np.pi / 2
pos = np.column_stack([np.cos(ang), np.sin(ang)]); x = pr(0.85)
for i, j in edges:
    ax[0].annotate("", xy=pos[j] * 0.92, xytext=pos[i] * 0.92, arrowprops=dict(arrowstyle="->", color="#888888", lw=0.9, shrinkA=9, shrinkB=9))
ax[0].scatter(*pos.T, s=x * 6000, color=BL, alpha=0.85, zorder=3)
for i in range(n): ax[0].text(*pos[i], labels[i], ha="center", va="center", color="white", fontsize=9, zorder=4, weight="bold")
ax[0].set_ylim(-1.25, 1.3); ax[0].set_title("12-page web, node area = PageRank (d = 0.85)"); ax[0].axis("off"); ax[0].set_aspect("equal")
w = 0.27
for k, (d, c) in enumerate([(0.5, TE), (0.85, BL), (0.99, OR)]):
    ax[1].bar(np.arange(n) + (k - 1) * w, pr(d), w, color=c, label=f"d = {d}")
ax[1].set_xticks(range(n)); ax[1].set_xticklabels(labels); ax[1].set_ylabel("PageRank"); ax[1].set_title("Damping study"); ax[1].legend()
plt.tight_layout(); plt.savefig("ch17_pagerank.png", dpi=110)
