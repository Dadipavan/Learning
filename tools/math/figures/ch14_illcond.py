import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 11})

grad = lambda p: np.array([p[0], 10 * p[1]])      # f = 0.5 (x^2 + 10 y^2), kappa = 10
start = np.array([9.0, 1.5])

def gd(alpha, steps):
    p = start.copy(); path = [p.copy()]
    for _ in range(steps):
        p = p - alpha * grad(p); path.append(p.copy())
    return np.array(path)

def mom(alpha, steps, beta=0.8):
    p = start.copy(); v = np.zeros(2); path = [p.copy()]
    for _ in range(steps):
        v = beta * v + grad(p); p = p - alpha * v; path.append(p.copy())
    return np.array(path)

X, Y = np.meshgrid(np.linspace(-2, 10, 300), np.linspace(-2.5, 2.5, 300))
Z = 0.5 * (X ** 2 + 10 * Y ** 2)
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.contour(X, Y, Z, levels=[1, 3, 6, 12, 20, 30, 40], colors="#bbbbbb", linewidths=1)
a = gd(0.18, 40); b = mom(0.05, 40)
ax.plot(a[:, 0], a[:, 1], color=ORANGE, marker="o", ms=3, lw=1.2, label="gradient descent, alpha = 0.18")
ax.plot(b[:, 0], b[:, 1], color=BLUE, marker="s", ms=3, lw=1.2, label="momentum, alpha = 0.05, beta = 0.8")
ax.plot(0, 0, marker="*", color=TEAL, ms=14, label="minimum")
ax.set_xlabel("x (gentle direction)"); ax.set_ylabel("y (steep direction)")
ax.set_title("A narrow valley: GD zig-zags across it, momentum smooths the path")
ax.legend(fontsize=9, loc="upper right")
plt.tight_layout(); plt.savefig("ch14_illcond.png", dpi=110)
