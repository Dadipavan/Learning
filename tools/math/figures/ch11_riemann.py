import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
f = lambda x: x**2
xs = np.linspace(0, 2, 200)
fig, axes = plt.subplots(1, 2, figsize=(8, 4.2), sharey=True)
for ax, n, kind, col in [(axes[0], 4, "left", "#b84a22"), (axes[1], 4, "mid", "#357a70")]:
    w = 2 / n
    left = np.arange(n) * w
    xp = left if kind == "left" else left + w / 2
    ax.bar(left, f(xp), width=w, align="edge", color=col, alpha=0.35, edgecolor=col)
    ax.plot(xs, f(xs), color="#2b4fd6", lw=2.2)
    total = f(xp).sum() * w
    ax.set_title(f"{kind} sum, n = 4: {total:.4f}", fontsize=12)
    ax.set_xlabel("x", fontsize=12); ax.grid(alpha=0.3)
axes[0].set_ylabel("f(x) = x²", fontsize=12)
fig.suptitle("Riemann sums for the area under x² on [0, 2] (exact 2.6667)", fontsize=13)
fig.tight_layout(); fig.savefig("ch11_riemann.png", dpi=110)
