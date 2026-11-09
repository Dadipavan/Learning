import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11})
x = np.linspace(-1, 5, 300)
fig, ax = plt.subplots(1, 3, figsize=(9, 3.8), sharey=True)
cases = [("x² − 4x + 3", 1, -4, 3, "D = 4 > 0: two roots", "#2b4fd6"),
         ("x² − 4x + 4", 1, -4, 4, "D = 0: one root", "#357a70"),
         ("x² − 4x + 5", 1, -4, 5, "D = −4 < 0: no real root", "#b84a22")]
for a, (t, p, q, r, s, c) in zip(ax, cases):
    a.plot(x, p * x**2 + q * x + r, color=c, lw=2)
    a.axhline(0, color="k", lw=.8); a.set_title(t, fontsize=10); a.set_xlabel(s, fontsize=9); a.grid(alpha=.3)
ax[0].plot([1, 3], [0, 0], "o", color="#aa2d26", ms=8)
ax[1].plot([2], [0], "o", color="#aa2d26", ms=8)
ax[0].set_ylim(-2, 6)
plt.tight_layout(); plt.savefig("ch01_quadratic.png", dpi=110)
