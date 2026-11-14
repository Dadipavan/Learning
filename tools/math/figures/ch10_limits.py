import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 3, figsize=(8, 4.2))
x = np.linspace(-12, 12, 800); x = x[x != 0]
axs[0].plot(x, np.sin(x) / x, color="#2b4fd6"); axs[0].plot([0], [1], "o", mfc="white", color="#2b4fd6")
axs[0].set_title("sin(x)/x → 1", fontsize=10)
x = np.linspace(-3, 3, 600); x = x[x != 0]
axs[1].plot(x[x < 0], np.abs(x[x < 0]) / x[x < 0], color="#aa2d26"); axs[1].plot(x[x > 0], np.abs(x[x > 0]) / x[x > 0], color="#aa2d26")
axs[1].plot([0, 0], [-1, 1], "o", mfc="white", color="#aa2d26"); axs[1].set_ylim(-1.6, 1.6)
axs[1].set_title("|x|/x: left −1, right +1", fontsize=10)
x = np.linspace(-0.3, 0.3, 4000); x = x[x != 0]
axs[2].plot(x, x * np.sin(1 / x), color="#357a70", lw=0.8)
axs[2].plot(x, np.abs(x), color="#b84a22", ls="--"); axs[2].plot(x, -np.abs(x), color="#b84a22", ls="--")
axs[2].set_title("squeeze: x·sin(1/x) → 0", fontsize=10)
for a in axs: a.grid(alpha=0.3); a.set_xlabel("x")
fig.tight_layout(); fig.savefig("ch10_limits.png", dpi=110)
