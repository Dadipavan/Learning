import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, 3, figsize=(8.6, 5.4))
x = np.linspace(-3, 3, 600)
def panel(a, y, t, c, step=False):
    a.plot(x if not step else x, y, color=c, lw=2); a.set_title(t, fontsize=10)
    a.axhline(0, color="k", lw=0.5); a.axvline(0, color="k", lw=0.5)
panel(ax[0, 0], np.maximum(0, x), "ReLU: max(0, x)", "#2b4fd6")
panel(ax[0, 1], np.where(x > 0, x, 0.1 * x), "Leaky ReLU (0.1)", "#357a70")
panel(ax[0, 2], np.abs(x), "Absolute value |x|", "#b84a22")
xs = np.linspace(-3, 3, 7)
ax[1, 0].step(x, (x >= 0).astype(float), where="post", color="#aa2d26", lw=2)
ax[1, 0].set_title("Step / indicator 1[x ≥ 0]", fontsize=10)
margin = np.linspace(-2, 3, 400)
ax[1, 1].plot(margin, np.maximum(0, 1 - margin), color="#6a2fd0", lw=2)
ax[1, 1].set_title("Hinge loss max(0, 1 − m)", fontsize=10); ax[1, 1].set_xlabel("margin m")
inc = np.linspace(0, 100, 1000)
tax = np.where(inc <= 20, 0, np.where(inc <= 50, 0.1 * (inc - 20), 3 + 0.3 * (inc - 50)))
ax[1, 2].plot(inc, tax, color="#2b4fd6", lw=2)
ax[1, 2].set_title("Tax brackets (income k → tax k)", fontsize=10); ax[1, 2].set_xlabel("income")
plt.tight_layout(); plt.savefig("ch02_piecewise.png", dpi=110)
