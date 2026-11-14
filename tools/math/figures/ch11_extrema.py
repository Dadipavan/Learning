import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
f = lambda x: x**3 - 6*x**2 + 9*x + 1
x = np.linspace(-0.5, 4.5, 400)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(x, f(x), color="#2b4fd6", lw=2.2, label="f(x) = x³ − 6x² + 9x + 1")
ax.axvspan(-0.5, 2, color="#aa2d26", alpha=0.08, label="concave down (f'' < 0)")
ax.axvspan(2, 4.5, color="#357a70", alpha=0.08, label="concave up (f'' > 0)")
ax.scatter([1], [f(1)], s=80, color="#aa2d26", zorder=5)
ax.scatter([3], [f(3)], s=80, color="#357a70", zorder=5)
ax.scatter([2], [f(2)], s=80, color="#6a2fd0", marker="D", zorder=5)
ax.annotate("local max (1, 5)", (1, 5), (0.0, 8.5), fontsize=11, arrowprops=dict(arrowstyle="->"))
ax.annotate("local min (3, 1)", (3, 1), (3.1, -2.5), fontsize=11, arrowprops=dict(arrowstyle="->"))
ax.annotate("inflection (2, 3)", (2, 3), (2.4, 7), fontsize=11, arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("x", fontsize=12); ax.set_ylabel("f(x)", fontsize=12)
ax.set_ylim(-5, 22); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=10)
ax.set_title("Critical points, concavity and the inflection point", fontsize=13)
fig.tight_layout(); fig.savefig("ch11_extrema.png", dpi=110)
