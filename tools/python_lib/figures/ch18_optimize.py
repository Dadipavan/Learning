import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

from scipy import optimize
def f(v): x, y = v; return (1 - x) ** 2 + 5 * (y - x ** 2) ** 2
path = [np.array([-1.2, 1.0])]
optimize.minimize(f, path[0], method="BFGS", callback=lambda xk: path.append(np.array(xk)))
path = np.array(path)
X, Y = np.meshgrid(np.linspace(-1.6, 1.6, 300), np.linspace(-0.5, 2.5, 300))
Z = (1 - X) ** 2 + 5 * (Y - X ** 2) ** 2
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
cs = ax.contour(X, Y, Z, levels=np.geomspace(0.05, 100, 14), colors="#7f95e0", linewidths=1.2)
ax.plot(path[:, 0], path[:, 1], "-o", color=O, lw=2, ms=5, label="BFGS steps")
ax.plot(1, 1, "*", color=R, ms=18, label="true minimum")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(frameon=False, loc="upper left")
ax.set_title("minimize walks down a curved valley")
fig.tight_layout(); fig.savefig("lib18_optimize.png")
