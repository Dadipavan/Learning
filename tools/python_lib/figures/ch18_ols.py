import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from scipy import stats
rng = np.random.default_rng(11)
x = rng.uniform(0, 10, 80)
y = 2 + 0.7 * x + rng.normal(0, 0.4 + 0.12 * x)
r = stats.linregress(x, y)
fit = r.intercept + r.slope * x
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110)
a1.scatter(x, y, color=O, s=22); xs = np.array([0, 10]); a1.plot(xs, r.intercept + r.slope * xs, color=B, lw=2.5)
a1.set_xlabel("x"); a1.set_ylabel("y"); a1.set_title("Line fit")
a2.scatter(fit, y - fit, color=T, s=22); a2.axhline(0, color="black", lw=1)
a2.set_xlabel("fitted value"); a2.set_ylabel("residual"); a2.set_title("Residuals fan out")
fig.tight_layout(); fig.savefig("lib18_ols.png")
