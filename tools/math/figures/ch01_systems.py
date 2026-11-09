import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11})
x = np.linspace(0, 10, 100)
fig, ax = plt.subplots(1, 2, figsize=(8.6, 4.2))
ax[0].plot(x, 10 - x, color="#2b4fd6", lw=2, label="a + b = 10")
ax[0].plot(x, (26 - 2 * x) / 4, color="#b84a22", lw=2, label="2a + 4b = 26")
ax[0].plot([7], [3], "o", color="#aa2d26", ms=9); ax[0].annotate("(7, 3)", (7.2, 3.4))
ax[0].set_xlim(0, 10); ax[0].set_ylim(0, 10); ax[0].set_xlabel("a"); ax[0].set_ylabel("b")
ax[0].set_title("Two equations: lines cross at the solution"); ax[0].legend(fontsize=9); ax[0].grid(alpha=.3)
y = 2 * x + 1
ax[1].plot(x, y, color="#357a70", lw=2); ax[1].fill_between(x, y, 25, color="#357a70", alpha=.2)
ax[1].fill_between(x, 0, 5 - 0 * x, color="#6a2fd0", alpha=.0)
ax[1].set_xlim(0, 10); ax[1].set_ylim(0, 25); ax[1].set_xlabel("x"); ax[1].set_ylabel("y")
ax[1].set_title("Inequality y > 2x + 1: a whole region"); ax[1].text(1, 18, "shaded: true", color="#357a70"); ax[1].grid(alpha=.3)
plt.tight_layout(); plt.savefig("ch01_systems.png", dpi=110)
