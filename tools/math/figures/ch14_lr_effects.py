import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 11})

def run(alpha, x0=4.0, steps=20):
    xs = [x0]
    for _ in range(steps):
        xs.append(xs[-1] * (1 - 2 * alpha))      # GD on f(x) = x^2
    return np.array(xs)

fig, ax = plt.subplots(1, 2, figsize=(9.6, 4.2))
for a, c, ls in ((0.01, PURPLE, "-"), (0.1, BLUE, "-"), (0.5, TEAL, "-"), (0.9, ORANGE, "--"), (1.0, "#555555", ":"), (1.05, RED, "-")):
    ax[0].plot(run(a), color=c, ls=ls, lw=2, marker="o", ms=3, label=f"alpha = {a}")
ax[0].set_ylim(-8, 8); ax[0].axhline(0, color="#999", lw=0.8)
ax[0].set_xlabel("iteration k"); ax[0].set_ylabel("x_k"); ax[0].set_title("f(x) = x^2, start x = 4")
ax[0].legend(fontsize=8, ncol=2, loc="upper right")

xx = np.linspace(-5, 5, 200)
ax[1].plot(xx, xx ** 2, color="#333", lw=1.5)
p = run(0.9, steps=6)
ax[1].plot(p, p ** 2, color=ORANGE, marker="o", lw=1.5, label="alpha = 0.9 (zig-zag, still shrinks)")
q = run(0.1, steps=6)
ax[1].plot(q, q ** 2, color=BLUE, marker="s", lw=1.5, label="alpha = 0.1 (smooth)")
ax[1].set_xlabel("x"); ax[1].set_ylabel("f(x)"); ax[1].set_title("The same steps drawn on the curve")
ax[1].legend(fontsize=8)
plt.tight_layout(); plt.savefig("ch14_lr_effects.png", dpi=110)
