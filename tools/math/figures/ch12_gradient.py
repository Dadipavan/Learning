import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
f = lambda X, Y: X**2 + 3*Y**2
g = np.linspace(-3.5, 3.5, 200); X, Y = np.meshgrid(g, g)
fig, ax = plt.subplots(figsize=(7, 5.2))
ax.contour(X, Y, f(X, Y), levels=[1, 3, 7, 12, 20, 30], colors="#2b4fd6", linewidths=1)
for (px, py) in [(2, 1), (-1, 1.5), (1, -1.5)]:
    gx, gy = 2*px, 6*py
    n = np.hypot(gx, gy)
    ax.annotate("", xy=(px + gx/n*1.0, py + gy/n*1.0), xytext=(px, py),
                arrowprops=dict(arrowstyle="->", color="#b84a22", lw=2))
    ax.plot([px], [py], "o", color="#aa2d26")
    tx, ty = -gy/n, gx/n
    ax.plot([px - tx*0.9, px + tx*0.9], [py - ty*0.9, py + ty*0.9], "--", color="#357a70", lw=1.5)
ax.text(2.1, 0.55, "(2, 1)\n∇f=(4, 6)", fontsize=9)
ax.plot([], [], color="#b84a22", label="gradient (steepest ascent)")
ax.plot([], [], "--", color="#357a70", label="tangent to contour")
ax.set_aspect("equal"); ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(loc="lower left", fontsize=8)
ax.set_title("f(x, y) = x² + 3y²: gradient is perpendicular to contours", fontsize=10)
fig.tight_layout(); fig.savefig("ch12_gradient.png", dpi=110)
