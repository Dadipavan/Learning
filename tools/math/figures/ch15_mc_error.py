import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rng = np.random.default_rng(3)
# target: P(Z > 4) for standard normal, true value 3.167124e-05
from scipy.stats import norm
truth = norm.sf(4.0)
Ns = [100, 300, 1000, 3000, 10000, 30000, 100000]
plain, imp = [], []
for N in Ns:
    pe, ie = [], []
    for _ in range(200):
        z = rng.standard_normal(N); pe.append(np.mean(z > 4))
        y = rng.normal(4, 1, N); w = np.exp(-4*y + 8)
        ie.append(np.mean((y > 4) * w))
    plain.append(np.sqrt(np.mean((np.array(pe)-truth)**2))/truth)
    imp.append(np.sqrt(np.mean((np.array(ie)-truth)**2))/truth)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.loglog(Ns, plain, "o-", color="#b84a22", label="plain Monte Carlo")
ax.loglog(Ns, imp, "s-", color="#2b4fd6", label="importance sampling, proposal Normal(4,1)")
ax.loglog(Ns, 3/np.sqrt(Ns), "--", color="k", lw=1, label="slope -1/2 reference")
ax.set_xlabel("number of samples N"); ax.set_ylabel("relative RMS error of estimate of P(Z > 4)")
ax.set_title("Rare event: importance sampling is far more accurate at equal N"); ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")
fig.tight_layout(); fig.savefig("ch15_mc_error.png", dpi=110)
