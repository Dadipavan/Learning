import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
g = np.linspace(-2, 2, 200); X, Y = np.meshgrid(g, g)
fs = [("Bowl: x² + y²\neigenvalues 2, 2", X**2 + Y**2),
      ("Saddle: x² − y²\neigenvalues 2, −2", X**2 - Y**2),
      ("Valley: x² + 0.1y²\neigenvalues 2, 0.2", X**2 + 0.1*Y**2)]
fig, axs = plt.subplots(1, 3, figsize=(10, 3.6))
for a, (t, Z) in zip(axs, fs):
    cs = a.contour(X, Y, Z, levels=12, cmap="coolwarm")
    a.plot([0], [0], "o", color="black"); a.set_title(t, fontsize=9)
    a.set_aspect("equal"); a.set_xlabel("x"); a.set_ylabel("y")
fig.tight_layout(); fig.savefig("ch12_hessian.png", dpi=110)
