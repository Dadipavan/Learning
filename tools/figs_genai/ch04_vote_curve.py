import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

from math import comb
def maj(p, n): return sum(comb(n, k) * p**k * (1 - p)**(n - k) for k in range(n // 2 + 1, n + 1))
p = np.linspace(0, 1, 201)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(p, p, color="#777", ls="--", label="single sample (n=1)")
for n, c in [(3, B), (5, O), (11, T), (31, P)]:
    ax.plot(p, [maj(x, n) for x in p], color=c, lw=2, label=f"vote over n={n}")
ax.scatter([0.6], [maj(0.6, 5)], color=R, zorder=5); ax.annotate("p=0.6, n=5: 0.683", (0.6, maj(0.6, 5)), (0.68, 0.45), arrowprops=dict(arrowstyle="->", color=R), color=R, fontsize=9)
ax.axvline(0.5, color="#bbb", lw=1)
ax.set_xlabel("accuracy of one sample (independent errors)"); ax.set_ylabel("accuracy of majority vote")
ax.set_title("Voting pushes accuracy away from 0.5, both ways")
ax.legend(frameon=False, fontsize=9); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch04d_vote_curve.png", dpi=110)
