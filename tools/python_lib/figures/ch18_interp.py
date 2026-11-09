import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from scipy import interpolate
xk = np.array([0, 1, 2, 3, 4, 5, 6.0]); yk = np.array([0, 0.8, 0.9, 0.1, -0.8, -1.0, -0.3])
xx = np.linspace(0, 6, 300)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.plot(xx, np.interp(xx, xk, yk), color=O, lw=2, label="np.interp (linear)")
ax.plot(xx, interpolate.CubicSpline(xk, yk)(xx), color=B, lw=2.5, label="CubicSpline")
ax.plot(xx, interpolate.PchipInterpolator(xk, yk)(xx), color=T, lw=2, ls="--", label="PCHIP")
ax.scatter(xk, yk, color="black", zorder=3, s=40, label="known points")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(frameon=False, fontsize=11)
ax.set_title("Three ways to fill the gaps")
fig.tight_layout(); fig.savefig("lib18_interp.png")
