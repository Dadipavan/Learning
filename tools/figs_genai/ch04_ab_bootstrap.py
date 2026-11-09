import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

rng = np.random.default_rng(4)
n = 200
a = rng.random(n) < 0.78
# prompt B fixes some of A's failures and breaks a few
b = a.copy()
fail = np.where(~a)[0]; b[rng.choice(fail, 14, replace=False)] = True
ok = np.where(a)[0]; b[rng.choice(ok, 4, replace=False)] = False
diffs = []
for _ in range(5000):
    i = rng.integers(0, n, n); diffs.append(b[i].mean() - a[i].mean())
diffs = np.array(diffs); lo, hi = np.percentile(diffs, [2.5, 97.5])
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.hist(100 * diffs, bins=40, color=B, alpha=0.8)
ax.axvline(0, color=R, ls="--"); ax.axvline(100 * lo, color=O); ax.axvline(100 * hi, color=O)
ax.text(100 * lo, ax.get_ylim()[1] * 0.92, f" 95% interval\n {100*lo:.1f} to {100*hi:.1f}", color=O, fontsize=9)
ax.text(0.1, ax.get_ylim()[1] * 0.6, " no change", color=R, fontsize=9)
ax.set_xlabel("accuracy(B) minus accuracy(A), points"); ax.set_ylabel("bootstrap resamples")
ax.set_title(f"Paired bootstrap: B wins 14, loses 4 of {n} cases")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch04d_ab_bootstrap.png", dpi=110)
print(round(100*lo,2), round(100*hi,2), round(100*(b.mean()-a.mean()),2))
