import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

xx = np.linspace(0, 2 * np.pi, 400)
target = np.sin(xx)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(xx, target, color="k", lw=2.5, label="target sin(x)")
for k, c in [(4, "#b84a22"), (8, "#2b4fd6"), (16, "#357a70")]:
    knots = np.linspace(0, 2 * np.pi, k + 1)
    vals = np.sin(knots)
    slopes = np.diff(vals) / np.diff(knots)
    # sum of ReLUs: start value + first slope, then slope changes at each knot
    y = vals[0] + slopes[0] * (xx - knots[0])
    for i in range(1, k):
        y = y + (slopes[i] - slopes[i - 1]) * np.maximum(0, xx - knots[i])
    ax.plot(xx, y, color=c, lw=1.6, label=f"{k} ReLU pieces")
ax.legend(); ax.set_xlabel("x"); ax.set_title("A sum of shifted ReLUs bends into any shape")
plt.tight_layout(); plt.savefig("ch02_relu_sum.png", dpi=110)
