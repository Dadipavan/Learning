import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
f = lambda x: np.exp(x) - 2 * x
x = np.linspace(-0.5, 2, 300); a = 1.0
q = f(a) + (np.exp(a) - 2) * (x - a) + 0.5 * np.exp(a) * (x - a) ** 2
lin = f(a) + (np.exp(a) - 2) * (x - a)
step = a - (np.exp(a) - 2) / np.exp(a)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(x, f(x), color="#2b4fd6", lw=2.4, label="loss f(x) = eˣ − 2x")
ax.plot(x, lin, color="#b84a22", lw=1.6, ls="--", label="linear approx at x = 1")
ax.plot(x, q, color="#357a70", lw=1.8, label="quadratic approx at x = 1")
ax.scatter([a], [f(a)], color="k", zorder=5); ax.scatter([step], [q.min()], color="#6a2fd0", s=70, zorder=5)
ax.annotate("Newton step lands at the\nbottom of the parabola", (step, q.min()), (1.2, 1.6), fontsize=10, arrowprops=dict(arrowstyle="->"))
ax.axvline(np.log(2), color="#aa2d26", lw=1, ls=":"); ax.text(np.log(2) - 0.05, 3.3, "true min ln 2", color="#aa2d26", ha="right", fontsize=10)
ax.set_ylim(0, 4); ax.set_xlabel("x", fontsize=12); ax.set_ylabel("loss", fontsize=12)
ax.grid(alpha=0.3); ax.legend(fontsize=10, loc="lower right")
ax.set_title("Second-order Taylor model of a loss, and the Newton step", fontsize=13)
fig.tight_layout(); fig.savefig("ch11_newton.png", dpi=110)
