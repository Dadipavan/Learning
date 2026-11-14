import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B, O, T = "#2b4fd6", "#b84a22", "#357a70"
plt.rcParams.update({"font.size": 11})
A = np.array([[4, 1, 0], [1, 5, 1], [0, 1, 3.]]); b = np.array([5, 7, 4.]); xt = np.ones(3)
x = np.zeros(3); ej = []
D = np.diag(A); Rm = A - np.diag(D)
for k in range(15):
    x = (b - Rm @ x) / D; ej.append(np.linalg.norm(x - xt))
x = np.zeros(3); eg = []; lr = 1 / np.linalg.eigvalsh(A).max()
for k in range(15):
    x = x - lr * (A @ x - b); eg.append(np.linalg.norm(x - xt))
fig, a = plt.subplots(figsize=(8, 4.2))
a.semilogy(range(1, 16), ej, "o-", color=B, lw=2, label="Jacobi")
a.semilogy(range(1, 16), eg, "s-", color=O, lw=2, label="gradient descent")
a.set_xlabel("iteration"); a.set_ylabel("distance to exact solution"); a.set_title("Iterative solvers shrink the error every step")
a.legend(); a.grid(alpha=.25, which="both")
fig.tight_layout(); fig.savefig("ch07_jacobi.png", dpi=110)
