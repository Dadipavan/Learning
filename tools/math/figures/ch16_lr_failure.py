import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# f(x) = 0.5*a*x^2 with a = 10; gradient descent x <- (1 - eta*a) x, start x=1
a = 10.0
fig, ax = plt.subplots(figsize=(8, 4.2))
for eta, col, lab in [(0.01, "#357a70", "eta = 0.01 (too small, factor 0.9)"),
                      (0.10, "#2b4fd6", "eta = 0.10 (factor 0, one step)"),
                      (0.19, "#6a2fd0", "eta = 0.19 (factor -0.9, slow zigzag)"),
                      (0.21, "#aa2d26", "eta = 0.21 (factor -1.1, diverges)")]:
    x = 1.0; vals = [0.5*a*x*x]
    for _ in range(25):
        x = (1 - eta*a)*x; vals.append(0.5*a*x*x)
    ax.semilogy(range(26), np.maximum(vals, 1e-12), "o-", ms=3, color=col, label=lab)
ax.set_xlabel("iteration"); ax.set_ylabel("loss f(x) (log scale)")
ax.set_title("Gradient descent on f(x) = 5x^2: stable only if eta < 2/a = 0.2")
ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")
fig.tight_layout(); fig.savefig("ch16_lr_failure.png", dpi=110)
