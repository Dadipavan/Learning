import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import factorial
fig, axes = plt.subplots(1, 2, figsize=(8, 4.2))
x = np.linspace(-2 * np.pi, 2 * np.pi, 500)
ax = axes[0]; ax.plot(x, np.sin(x), "k", lw=2.2, label="sin x")
for deg, c in [(1, "#b84a22"), (3, "#357a70"), (5, "#6a2fd0"), (9, "#2b4fd6")]:
    y = sum((-1) ** k * x ** (2 * k + 1) / factorial(2 * k + 1) for k in range((deg - 1) // 2 + 1))
    ax.plot(x, y, color=c, lw=1.6, label=f"degree {deg}")
ax.set_ylim(-3, 3); ax.set_title("sin x: converges everywhere", fontsize=12); ax.legend(fontsize=9); ax.grid(alpha=0.3)
ax = axes[1]; x = np.linspace(-0.9, 2.5, 500); ax.plot(x, np.log1p(x), "k", lw=2.2, label="ln(1 + x)")
for deg, c in [(3, "#b84a22"), (7, "#6a2fd0"), (15, "#2b4fd6")]:
    y = sum((-1) ** (k - 1) * x ** k / k for k in range(1, deg + 1))
    ax.plot(x, y, color=c, lw=1.6, label=f"degree {deg}")
ax.axvline(1, color="#aa2d26", ls="--", lw=1); ax.text(1.03, -1.4, "radius 1", color="#aa2d26", fontsize=10)
ax.set_ylim(-2, 2); ax.set_title("ln(1 + x): breaks past |x| = 1", fontsize=12); ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("ch11_taylor.png", dpi=110)
