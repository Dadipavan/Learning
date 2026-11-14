import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(8, 4.2))
n = np.arange(0, 31)
for r, c in [(0.5, "#2b4fd6"), (0.9, "#357a70"), (-0.8, "#6a2fd0")]:
    s = np.cumsum(r ** n)
    ax[0].plot(n, s, "o-", ms=3, color=c, label=f"r = {r}, limit = {1/(1-r):.2f}")
    ax[0].axhline(1 / (1 - r), color=c, ls=":", lw=1)
ax[0].set_title("Converges when |r| < 1", fontsize=11)
ax[0].set_xlabel("number of terms n"); ax[0].set_ylabel("partial sum S"); ax[0].legend(fontsize=8)
m = np.arange(0, 13)
for r, c in [(1.0, "#357a70"), (1.2, "#b84a22"), (-1.1, "#aa2d26")]:
    ax[1].plot(m, np.cumsum(r ** m), "o-", ms=3, color=c, label=f"r = {r}")
ax[1].set_title("Diverges when |r| ≥ 1", fontsize=11)
ax[1].set_xlabel("number of terms n"); ax[1].legend(fontsize=8)
for a in ax: a.grid(alpha=.3)
plt.tight_layout(); plt.savefig("ch04_geometric.png", dpi=110)
