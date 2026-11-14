import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rng = np.random.default_rng(7)
fig, axs = plt.subplots(1, 2, figsize=(9, 4.2))
ax = axs[0]
for i in range(5):
    x = rng.exponential(1.0, 5000)
    ax.plot(np.arange(1, 5001), np.cumsum(x) / np.arange(1, 5001), lw=1.2)
ax.axhline(1.0, color="k", ls="--", lw=1)
ax.set_xscale("log"); ax.set_xlabel("sample size n"); ax.set_ylabel("sample mean")
ax.set_title("LLN: running means of Exponential(1)"); ax.grid(alpha=0.3)
ax = axs[1]
n = 30
m = rng.exponential(1.0, (20000, n)).mean(axis=1)
ax.hist(m, bins=60, density=True, color="#2b4fd6", alpha=0.6, label="means of n=30")
g = np.linspace(0.3, 2.0, 300)
ax.plot(g, np.exp(-(g-1)**2 / (2/n)) / np.sqrt(2*np.pi/n), color="#b84a22", lw=2, label="Normal(1, 1/30)")
ax.set_xlabel("sample mean"); ax.set_title("CLT: skewed data, near-normal means"); ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("ch15_clt_lln.png", dpi=110)
