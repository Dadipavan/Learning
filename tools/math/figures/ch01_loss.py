import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11})
y = np.array([3.0, 5.0, 10.0])
c = np.linspace(0, 12, 200)
loss = ((y[None, :] - c[:, None]) ** 2).mean(axis=1)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(c, loss, color="#2b4fd6", lw=2, label="mean squared error of guess c")
ax.plot([6], [((y - 6) ** 2).mean()], "o", color="#aa2d26", ms=9)
ax.annotate("minimum at the mean, c = 6", (6, 8.67), (7.2, 25), arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("constant guess c"); ax.set_ylabel("MSE"); ax.set_title("Completing the square: the loss is a parabola whose vertex is the mean")
ax.title.set_fontsize(10); ax.grid(alpha=.3); ax.legend()
plt.tight_layout(); plt.savefig("ch01_loss.png", dpi=110)
