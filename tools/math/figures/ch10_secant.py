import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
f = lambda x: x**2
x = np.linspace(-0.3, 3.3, 300)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(x, f(x), color="#2b4fd6", lw=2.5, label="f(x) = x²")
for h, c in [(1.5, "#aa2d26"), (0.7, "#b84a22"), (0.25, "#6a2fd0")]:
    m = (f(1 + h) - f(1)) / h
    xs = np.linspace(-0.3, 3.3, 10)
    ax.plot(xs, f(1) + m * (xs - 1), color=c, lw=1.4, ls="--", label=f"secant h={h}: slope {m:.2f}")
    ax.plot([1 + h], [f(1 + h)], "o", color=c)
xs = np.linspace(-0.3, 3.3, 10)
ax.plot(xs, 1 + 2 * (xs - 1), color="#357a70", lw=2.2, label="tangent: slope 2")
ax.plot([1], [1], "ko")
ax.set_ylim(-0.5, 8); ax.set_xlim(-0.3, 3.3)
ax.set_xlabel("x"); ax.set_ylabel("f(x)"); ax.set_title("Secants rotate into the tangent as h shrinks", fontsize=12)
ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("ch10_secant.png", dpi=110)
