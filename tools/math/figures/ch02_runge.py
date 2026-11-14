import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

f = lambda x: 1 / (1 + 25 * x**2)
xx = np.linspace(-1, 1, 400)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(xx, f(xx), color="k", lw=2.5, label="true f(x) = 1/(1+25x²)")
for n, c in [(5, "#357a70"), (9, "#2b4fd6"), (15, "#aa2d26")]:
    xn = np.linspace(-1, 1, n)
    coef = np.polyfit(xn, f(xn), n - 1)
    ax.plot(xx, np.polyval(coef, xx), color=c, lw=1.6, label=f"degree {n-1} through {n} points")
    ax.scatter(xn, f(xn), color=c, s=14, zorder=5)
ax.set_ylim(-1, 1.6); ax.legend(fontsize=8); ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title("Runge phenomenon: more points, wilder edges")
plt.tight_layout(); plt.savefig("ch02_runge.png", dpi=110)
