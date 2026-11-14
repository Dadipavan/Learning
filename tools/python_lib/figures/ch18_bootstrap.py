import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from scipy import stats
rng = np.random.default_rng(3)
data = rng.lognormal(1.2, 0.5, 60)
res = stats.bootstrap((data,), np.median, n_resamples=5000, random_state=1, method="percentile")
lo, hi = res.confidence_interval
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.hist(res.bootstrap_distribution, bins=40, color="#c9d3f5")
ax.axvline(np.median(data), color=B, lw=2.5, label="sample median")
ax.axvline(lo, color=R, lw=2.5, ls="--", label="95% interval")
ax.axvline(hi, color=R, lw=2.5, ls="--")
ax.set_xlabel("median of a resample"); ax.set_ylabel("count"); ax.legend(frameon=False)
ax.set_title("Bootstrap: 5000 medians from resampled data")
fig.tight_layout(); fig.savefig("lib18_bootstrap.png")
