import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2, figsize=(8, 4.2))
x = np.linspace(-3, 5, 200)
for m, b, c in [(2, 1, "#2b4fd6"), (0.5, 1, "#357a70"), (-1, 1, "#b84a22")]:
    ax[0].plot(x, m * x + b, color=c, lw=2, label=f"y = {m}x + 1")
ax[0].scatter([0], [1], color="black", zorder=5)
ax[0].annotate("intercept (0, 1)", (0, 1), (0.6, -2.2), arrowprops=dict(arrowstyle="->"))
ax[0].set_ylim(-4, 8); ax[0].set_title("Lines: slope tilts, intercept anchors")
ax[0].axhline(0, color="grey", lw=0.8); ax[0].axvline(0, color="grey", lw=0.8)
ax[0].legend(); ax[0].set_xlabel("x"); ax[0].set_ylabel("y")

x = np.linspace(-1, 5, 200)
y = x**2 - 4 * x + 3
ax[1].plot(x, y, color="#6a2fd0", lw=2, label="y = x² − 4x + 3")
ax[1].scatter([2], [-1], color="#aa2d26", zorder=5, s=50)
ax[1].annotate("vertex (2, −1)", (2, -1), (2.5, 3), arrowprops=dict(arrowstyle="->"))
ax[1].scatter([1, 3], [0, 0], color="#357a70", zorder=5)
ax[1].annotate("roots 1 and 3", (3, 0), (3.3, 6), arrowprops=dict(arrowstyle="->"))
ax[1].axvline(2, color="grey", ls="--", lw=1)
ax[1].axhline(0, color="grey", lw=0.8)
ax[1].set_title("Parabola: vertex and roots"); ax[1].legend(loc="upper center")
ax[1].set_xlabel("x"); ax[1].set_ylabel("y")
plt.tight_layout(); plt.savefig("ch02_lines_parabola.png", dpi=110)
