import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rng = np.random.default_rng(0)
n = 100
G = rng.normal(size=(n, n)) / np.sqrt(n)
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
ax = axs[0]
ev = np.linalg.eigvals(G)
ax.scatter(ev.real, ev.imag, s=12, color="#2b4fd6")
a = np.linspace(0, 2 * np.pi, 200); ax.plot(np.cos(a), np.sin(a), color="#aa2d26", lw=1.2)
ax.set_aspect("equal"); ax.set_title("Eigenvalues of a random 100x100 matrix\nfill a disc of radius 1"); ax.set_xlabel("real"); ax.set_ylabel("imaginary"); ax.grid(alpha=.3)
ax = axs[1]
for g, c in [(0.9, "#357a70"), (1.0, "#2b4fd6"), (1.1, "#b84a22")]:
    x = rng.normal(size=n); x /= np.linalg.norm(x); norms = [1.0]
    for _ in range(100):
        x = g * G @ x; norms.append(np.linalg.norm(x))
    ax.semilogy(norms, color=c, lw=2, label=f"gain g = {g}")
ax.set_xlabel("steps (same matrix applied repeatedly)"); ax.set_ylabel("norm of signal"); ax.set_title("Repeated multiplication: vanish or explode"); ax.legend(); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig("ch08_random_depth.png", dpi=110)
