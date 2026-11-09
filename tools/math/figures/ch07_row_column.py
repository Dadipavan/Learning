import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 11})
fig, ax = plt.subplots(1, 2, figsize=(8.6, 4.2))
x = np.linspace(-1, 5, 50)
a = ax[0]
a.plot(x, 3 - x, color=B, lw=2, label="x + y = 3")
a.plot(x, x - 1, color=O, lw=2, label="x − y = 1")
a.plot([2], [1], "o", color=R, ms=9)
a.annotate("solution (2, 1)", (2, 1), (2.6, 2.4), arrowprops=dict(arrowstyle="->"))
a.set_xlim(-1, 5); a.set_ylim(-2, 4); a.axhline(0, color="#888", lw=.6); a.axvline(0, color="#888", lw=.6)
a.set_title("Row picture: two lines meet"); a.legend(loc="lower left"); a.set_xlabel("x"); a.set_ylabel("y"); a.grid(alpha=.25)
a = ax[1]
def arr(p, q, c, lab=None, ls="-"):
    a.annotate("", q, p, arrowprops=dict(arrowstyle="->", color=c, lw=2.2, ls=ls))
arr((0, 0), (2, 2), B)
a.text(0.6, 1.5, "2 × col 1\n= (2, 2)", color=B)
arr((2, 2), (3, 1), O)
a.text(2.75, 1.9, "1 × col 2\n= (1, −1)", color=O)
arr((0, 0), (3, 1), R)
a.text(1.0, 0.1, "b = (3, 1)", color=R)
a.set_xlim(-0.5, 4.5); a.set_ylim(-0.5, 3); a.set_aspect("equal"); a.grid(alpha=.25)
a.set_title("Column picture: a recipe of columns"); a.set_xlabel("first coordinate"); a.set_ylabel("second coordinate")
fig.tight_layout(); fig.savefig("ch07_row_column.png", dpi=110)
