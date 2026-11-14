import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from scipy import optimize, stats
rng = np.random.default_rng(5)
def f(t, a, k, c): return a * np.exp(-k * t) + c
t = np.linspace(0, 10, 30)
y = f(t, 4.0, 0.5, 1.0) + rng.normal(0, 0.15, t.size)
p, cov = optimize.curve_fit(f, t, y, p0=[1, 1, 0])
tt = np.linspace(0, 10, 200)
J = np.empty((tt.size, 3))
for j in range(3):
    d = np.zeros(3); d[j] = 1e-6 * max(1, abs(p[j]))
    J[:, j] = (f(tt, *(p + d)) - f(tt, *p)) / d[j]
se = np.sqrt(np.einsum("ij,jk,ik->i", J, cov, J))
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.scatter(t, y, color=O, s=35, label="measurements", zorder=3)
ax.plot(tt, f(tt, *p), color=B, lw=2.5, label="curve_fit")
ax.fill_between(tt, f(tt, *p) - 1.96 * se, f(tt, *p) + 1.96 * se, color=B, alpha=0.2, label="approx. 95% band")
ax.set_xlabel("time"); ax.set_ylabel("signal"); ax.legend(frameon=False)
ax.set_title("Curve fit with an uncertainty band")
fig.tight_layout(); fig.savefig("lib18_curvefit.png")
