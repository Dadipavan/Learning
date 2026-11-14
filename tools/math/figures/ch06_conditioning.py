import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
x = np.linspace(0, 3, 100)
cases = [(np.array([[1, 1], [1, -1.0]]), "Well conditioned (lines cross at a right angle)"),
         (np.array([[1, 1], [1, 1.02]]), "Nearly singular (almost parallel lines)")]
for ax, (A, title) in zip(axes, cases):
    for b2, ls, col in [(2.0, "-", RED), (2.02, "--", PURPLE)]:
        b = np.array([2.0, b2])
        sol = np.linalg.solve(A, b)
        ax.plot(x, 2 - x, color=BLUE, ls=ls, lw=1.8)
        ax.plot(x, (b2 - A[1, 0] * x) / A[1, 1], color=ORANGE, ls=ls, lw=1.8)
        ax.plot(*sol, "o", color=col, ms=9, label=f"b2 = {b2}: solution ({sol[0]:.2f}, {sol[1]:.2f})")
    ax.set_ylim(-1.5, 3.5); ax.set_xlim(0, 3); ax.grid(alpha=0.3)
    ax.set_title(f"{title}\ncondition number = {np.linalg.cond(A):.0f}", fontsize=10)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(fontsize=8, loc="upper right")
fig.tight_layout()
fig.savefig("ch06_conditioning.png", dpi=110)
