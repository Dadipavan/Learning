import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
f = np.sin; exact = 2.0
ns = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
trap, simp, mc = [], [], []
rng = np.random.default_rng(0)
for n in ns:
    x = np.linspace(0, np.pi, n + 1); h = np.pi / n; y = f(x)
    trap.append(abs(h * (y.sum() - 0.5 * (y[0] + y[-1])) - exact))
    s = h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())
    simp.append(max(abs(s - exact), 1e-17))
    errs = [abs(np.pi * f(rng.uniform(0, np.pi, n)).mean() - exact) for _ in range(200)]
    mc.append(np.mean(errs))
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.loglog(ns, trap, "o-", color="#2b4fd6", label="trapezoid (error ~ n⁻²)")
ax.loglog(ns, simp, "s-", color="#357a70", label="Simpson (error ~ n⁻⁴)")
ax.loglog(ns, mc, "^-", color="#b84a22", label="Monte Carlo (error ~ n⁻½)")
ax.set_xlabel("number of function evaluations n", fontsize=12)
ax.set_ylabel("absolute error", fontsize=12)
ax.set_title("Integrating sin(x) on [0, π]: error versus work", fontsize=13)
ax.grid(alpha=0.3, which="both"); ax.legend(fontsize=10)
fig.tight_layout(); fig.savefig("ch11_integration_error.png", dpi=110)
