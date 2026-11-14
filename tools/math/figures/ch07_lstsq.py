import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 11})
fig, ax = plt.subplots(1, 2, figsize=(9, 4.2))
x = np.array([1, 2, 3, 4.]); y = np.array([1, 3, 4, 4.])
a = ax[0]
xs = np.linspace(0.5, 4.5, 10)
a.plot(xs, 0.5 + xs, color=B, lw=2, label="best line  y = 0.5 + 1·x")
a.plot(x, y, "o", color=O, ms=9, label="data")
for xi, yi in zip(x, y):
    a.plot([xi, xi], [yi, 0.5 + xi], color=R, lw=2)
a.plot(x, 0.5 + x, "s", color=T, ms=6, label="fitted values")
a.set_title("Fit a line: shrink the red errors"); a.set_xlabel("x"); a.set_ylabel("y"); a.legend(loc="upper left", fontsize=9); a.grid(alpha=.25)
a = ax[1]
av = np.array([2, 1.]); b = np.array([1, 2.]); p = av.dot(b) / av.dot(av) * av
t = np.linspace(-0.6, 3, 5); a.plot(t * 2, t, color=B, lw=1.5, ls="--")
def arr(q, c, p0=(0, 0)):
    a.annotate("", q, p0, arrowprops=dict(arrowstyle="->", color=c, lw=2.4))
arr(b, O); arr(p, B); arr(b, R, p0=tuple(p))
a.text(0.5, 1.6, "b", color=O, fontsize=13); a.text(1.7, 0.55, "p = A x̂", color=B, fontsize=12)
a.text(1.45, 1.5, "e = b − p", color=R, fontsize=12)
a.plot([p[0] - 0.12, p[0] - 0.12 + 0.05 * 0 ], [p[1] + 0.24, p[1] + 0.24], alpha=0)
a.text(3.2, 1.2, "column space\n(a line here)", color=B, fontsize=10, ha="center")
a.set_xlim(-0.5, 4.2); a.set_ylim(-0.5, 2.7); a.set_aspect("equal"); a.grid(alpha=.25)
a.set_title("Projection: e is perpendicular to p")
fig.tight_layout(); fig.savefig("ch07_lstsq.png", dpi=110)
