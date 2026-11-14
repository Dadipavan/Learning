import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import comb
fig, ax = plt.subplots(1, 2, figsize=(8, 4.2), gridspec_kw={"width_ratios": [1, 1.1]})
for n in range(7):
    for k in range(n + 1):
        ax[0].text(k - n / 2, -n, str(comb(n, k)), ha="center", va="center", fontsize=11,
                   color="#2b4fd6" if k in (0, n) else "#222")
ax[0].set_xlim(-3.7, 3.7); ax[0].set_ylim(-6.7, 0.7); ax[0].axis("off")
ax[0].set_title("Pascal's triangle (each = sum of two above)", fontsize=10)
k = np.arange(11)
ax[1].bar(k, [comb(10, i) for i in k], color="#357a70")
for i in k: ax[1].text(i, comb(10, i) + 4, str(comb(10, i)), ha="center", fontsize=8)
ax[1].set_title("Row n = 10: C(10, k), total 2^10 = 1024", fontsize=10)
ax[1].set_xlabel("k (items chosen)"); ax[1].set_ylabel("ways"); ax[1].grid(alpha=.3, axis="y")
plt.tight_layout(); plt.savefig("ch04_pascal.png", dpi=110)
