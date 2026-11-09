import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 11})

def rosen(p):  return (1 - p[0]) ** 2 + 100 * (p[1] - p[0] ** 2) ** 2
def grad(p):
    return np.array([-2 * (1 - p[0]) - 400 * p[0] * (p[1] - p[0] ** 2), 200 * (p[1] - p[0] ** 2)])

def gd(alpha, steps, p0=(-1.5, 1.5)):
    p = np.array(p0); path = [p.copy()]
    for _ in range(steps):
        p = p - alpha * grad(p); path.append(p.copy())
    return np.array(path)

def momentum(alpha, steps, beta=0.9, p0=(-1.5, 1.5)):
    p = np.array(p0); v = np.zeros(2); path = [p.copy()]
    for _ in range(steps):
        v = beta * v + grad(p); p = p - alpha * v; path.append(p.copy())
    return np.array(path)

def rmsprop(alpha, steps, rho=0.9, eps=1e-8, p0=(-1.5, 1.5)):
    p = np.array(p0); s = np.zeros(2); path = [p.copy()]
    for _ in range(steps):
        g = grad(p); s = rho * s + (1 - rho) * g * g
        p = p - alpha * g / (np.sqrt(s) + eps); path.append(p.copy())
    return np.array(path)

def adam(alpha, steps, b1=0.9, b2=0.999, eps=1e-8, p0=(-1.5, 1.5)):
    p = np.array(p0); m = np.zeros(2); v = np.zeros(2); path = [p.copy()]
    for t in range(1, steps + 1):
        g = grad(p); m = b1 * m + (1 - b1) * g; v = b2 * v + (1 - b2) * g * g
        p = p - alpha * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + eps); path.append(p.copy())
    return np.array(path)

X, Y = np.meshgrid(np.linspace(-2, 2, 400), np.linspace(-0.5, 2.2, 400))
Z = (1 - X) ** 2 + 100 * (Y - X ** 2) ** 2
fig, (ax, bx) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={'width_ratios': [1.25, 1]})
ax.contour(X, Y, np.log10(Z + 1e-9), levels=np.linspace(-1, 3.5, 14), colors="#c8c8c8", linewidths=0.9)
for path, c, lab in ((gd(0.001, 5000), ORANGE, "GD 0.001"), (momentum(0.0002, 5000), PURPLE, "Momentum 0.0002"),
                     (rmsprop(0.005, 5000), TEAL, "RMSProp 0.005"), (adam(0.05, 5000), BLUE, "Adam 0.05")):
    ax.plot(path[:, 0], path[:, 1], color=c, lw=1.4, label=lab)
    bx.semilogy(np.maximum([rosen(p) for p in path], 1e-16), color=c, lw=1.6, label=lab)
ax.plot(1, 1, marker="*", color=RED, ms=15, label="minimum (1, 1)")
ax.plot(-1.5, 1.5, marker="o", color="#333", ms=6)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_title("Paths in the banana valley")
bx.set_xlabel("step"); bx.set_ylabel("loss (log scale, floor 1e-16)"); bx.set_title("Loss against step"); bx.legend(fontsize=8)
ax.legend(fontsize=8, loc="lower right")
plt.tight_layout(); plt.savefig("ch14_optimizers.png", dpi=110)
