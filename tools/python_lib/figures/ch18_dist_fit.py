import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from scipy import stats
rng = np.random.default_rng(7)
data = rng.lognormal(mean=1.2, sigma=0.5, size=800)
s, loc, sc = stats.lognorm.fit(data, floc=0)
mu, sd = stats.norm.fit(data)
x = np.linspace(0, data.max(), 300)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.hist(data, bins=40, density=True, color="#c9d3f5", label="data (800 delivery times)")
ax.plot(x, stats.lognorm.pdf(x, s, loc, sc), color=B, lw=2.5, label="lognormal fit")
ax.plot(x, stats.norm.pdf(x, mu, sd), color=O, lw=2.5, ls="--", label="normal fit")
ax.set_xlabel("delivery time (hours)"); ax.set_ylabel("density"); ax.legend(frameon=False)
ax.set_title("Skewed data: the lognormal fits, the normal does not")
fig.tight_layout(); fig.savefig("lib18_dist_fit.png")
