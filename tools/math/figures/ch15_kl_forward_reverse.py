import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
x = np.linspace(-9, 9, 2000); dx = x[1]-x[0]
def N(x, m, s): return np.exp(-(x-m)**2/(2*s*s))/(s*np.sqrt(2*np.pi))
p = 0.5*N(x, -3, 1) + 0.5*N(x, 3, 1)
best_f = best_r = None; bf = br = 1e9
eps = 1e-300
for m in np.linspace(-5, 5, 101):
    for s in np.linspace(0.5, 5, 91):
        q = N(x, m, s)
        f = np.sum(p*np.log((p+eps)/(q+eps)))*dx
        r = np.sum(q*np.log((q+eps)/(p+eps)))*dx
        if f < bf: bf, best_f = f, (m, s)
        if r < br and m > 0: br, best_r = r, (m, s)
fig, axs = plt.subplots(1, 2, figsize=(9, 4.0), sharey=True)
for ax, (m, s), ttl, c in zip(axs, [best_f, best_r], ["Forward KL(p||q): covers both modes", "Reverse KL(q||p): locks on one mode"], ["#b84a22", "#357a70"]):
    ax.fill_between(x, p, color="#2b4fd6", alpha=0.3, label="p: two peaks")
    ax.plot(x, N(x, m, s), color=c, lw=2.2, label=f"q: Normal({m:.1f}, {s:.1f})")
    ax.set_title(ttl, fontsize=10); ax.legend(fontsize=8); ax.grid(alpha=0.3); ax.set_xlabel("x")
fig.tight_layout(); fig.savefig("ch15_kl_forward_reverse.png", dpi=110)
