import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(8, 4.2))
n = np.arange(1, 81)
p = [1 - np.prod((365 - np.arange(k)) / 365) for k in n]
ax[0].plot(n, p, color="#2b4fd6"); ax[0].axhline(0.5, ls=":", color="#aa2d26")
ax[0].axvline(23, ls=":", color="#aa2d26"); ax[0].text(25, 0.1, "n = 23 gives 50.7%", fontsize=9)
ax[0].set_title("Birthday problem (365 days)", fontsize=11); ax[0].set_xlabel("people n"); ax[0].set_ylabel("P(shared birthday)")
k = np.logspace(2, 6, 200); M = 2.0 ** 32
ax[1].plot(k, 1 - np.exp(-k * (k - 1) / (2 * M)), color="#b84a22")
ax[1].set_xscale("log"); ax[1].axvline(77163, ls=":", color="#aa2d26")
ax[1].set_title("32-bit hash: P(any collision)", fontsize=11); ax[1].set_xlabel("number of keys (log scale)")
for a in ax: a.grid(alpha=.3)
plt.tight_layout(); plt.savefig("ch04_birthday.png", dpi=110)
