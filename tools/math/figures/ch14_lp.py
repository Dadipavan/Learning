import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 11})

x = np.linspace(0, 60, 200)
fig, ax = plt.subplots(figsize=(8, 4.8))
ax.plot(x, 100 - 2 * x, color=BLUE, lw=2, label="oven: 2x + y = 100")
ax.plot(x, (120 - x) / 3, color=ORANGE, lw=2, label="labour: x + 3y = 120")
verts = np.array([[0, 0], [50, 0], [36, 28], [0, 40]])
ax.fill(verts[:, 0], verts[:, 1], color=TEAL, alpha=0.2, label="feasible region")
for v in verts:
    ax.plot(*v, "o", color="#222"); ax.annotate(f"({v[0]}, {v[1]}): {40*v[0]+30*v[1]}", v, textcoords="offset points", xytext=(6, 6), fontsize=9)
for P in (1200, 1800, 2280):
    ax.plot(x, (P - 40 * x) / 30, color=PURPLE, lw=1, ls="--", alpha=0.8)
ax.annotate("profit 40x + 30y = 2280", (41, 22), color=PURPLE, fontsize=9, rotation=-33)
ax.plot(36, 28, "*", color=RED, ms=16, label="optimum")
ax.set_xlim(0, 60); ax.set_ylim(0, 70)
ax.set_xlabel("x = trays of croissants"); ax.set_ylabel("y = loaves")
ax.set_title("Product mix: the best profit sits at a corner"); ax.legend(fontsize=9, loc="upper right")
plt.tight_layout(); plt.savefig("ch14_lp.png", dpi=110)
