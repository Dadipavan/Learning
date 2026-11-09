import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 10})
fig, ax = plt.subplots(1, 3, figsize=(9.6, 3.6))
x = np.linspace(-1, 5, 50)
a = ax[0]; a.plot(x, 3 - x, color=B, lw=2); a.plot(x, x - 1, color=O, lw=2); a.plot([2], [1], "o", color=R, ms=9)
a.set_title("Unique: lines cross\nrank 2 = unknowns 2")
a = ax[1]; a.plot(x, 3 - x, color=B, lw=2); a.plot(x, 5 - x, color=O, lw=2)
a.set_title("None: parallel lines\nx + y = 3 and x + y = 5")
a = ax[2]; a.plot(x, 3 - x, color=B, lw=5, alpha=.6); a.plot(x, (6 - 2 * x) / 2, color=O, lw=2, ls="--")
a.set_title("Infinite: same line\nx + y = 3 and 2x + 2y = 6")
for a in ax:
    a.set_xlim(-1, 5); a.set_ylim(-2, 5); a.axhline(0, color="#888", lw=.6); a.axvline(0, color="#888", lw=.6); a.grid(alpha=.25)
fig.tight_layout(); fig.savefig("ch07_outcomes.png", dpi=110)
