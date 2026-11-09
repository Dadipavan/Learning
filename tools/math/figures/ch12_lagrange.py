import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
g = np.linspace(0, 10, 300); X, Y = np.meshgrid(g, g)
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
a = axs[0]
cs = a.contour(X, Y, X*Y, levels=[5, 10, 15, 20, 25, 30], colors="#2b4fd6")
a.clabel(cs, fontsize=8)
a.plot(g, 10 - g, color="#b84a22", lw=2.5, label="constraint x + y = 10")
a.plot([5], [5], "o", color="#aa2d26", ms=9, label="best point (5, 5)")
a.annotate("", xy=(6, 6), xytext=(5, 5), arrowprops=dict(arrowstyle="->", color="#357a70", lw=2))
a.text(6.1, 6.0, "∇f ∥ ∇g", fontsize=9, color="#357a70")
a.set_xlim(0, 10); a.set_ylim(0, 10); a.set_aspect("equal")
a.set_title("Maximise xy on a line: the contour just touches", fontsize=10)
a.set_xlabel("x"); a.set_ylabel("y"); a.legend(fontsize=8, loc="upper right")
b = axs[1]
P = np.linspace(4, 40, 100)
b.plot(P, P**2/16, color="#2b4fd6", lw=2, label="best area A*(P) = P²/16")
p0 = 20; slope = p0/8
b.plot(P, 25 + slope*(P - p0), "--", color="#b84a22", label="tangent, slope λ = 2.5")
b.plot([p0], [25], "o", color="#aa2d26")
b.set_xlabel("perimeter P"); b.set_ylabel("best area"); b.set_ylim(0, 110)
b.set_title("λ is the shadow price: slope of the best value", fontsize=10); b.legend(fontsize=8)
fig.tight_layout(); fig.savefig("ch12_lagrange.png", dpi=110)
