import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
x = np.linspace(-6, 6, 600)
sig = 1 / (1 + np.exp(-x)); th = np.tanh(x); relu = np.maximum(0, x); sp = np.log1p(np.exp(x))
fig, axs = plt.subplots(1, 2, figsize=(8, 4.2), sharex=True)
for y, n, c in [(sig, "sigmoid", "#2b4fd6"), (th, "tanh", "#b84a22"), (relu, "ReLU", "#357a70"), (sp, "softplus", "#6a2fd0")]:
    axs[0].plot(x, y, color=c, lw=2, label=n)
axs[0].set_title("Functions", fontsize=11); axs[0].set_ylim(-1.5, 4)
d = {"sigmoid": sig * (1 - sig), "tanh": 1 - th**2, "ReLU": (x > 0).astype(float), "softplus": sig}
for (n, c) in [("sigmoid", "#2b4fd6"), ("tanh", "#b84a22"), ("ReLU", "#357a70"), ("softplus", "#6a2fd0")]:
    axs[1].plot(x, d[n], color=c, lw=2, label=n)
axs[1].set_title("Derivatives", fontsize=11); axs[1].set_ylim(-0.1, 1.15)
for a in axs: a.grid(alpha=0.3); a.set_xlabel("x"); a.legend(fontsize=9)
fig.tight_layout(); fig.savefig("ch10_activations.png", dpi=110)
