import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11})
fig, ax = plt.subplots(1, 2, figsize=(8.6, 4.2))
m = np.arange(0, 25)
ax[0].plot(m, 1000 * (1 + 0.05 * m), color="#b84a22", lw=2, label="simple: +5% of the start each month")
ax[0].plot(m, 1000 * 1.05 ** m, color="#2b4fd6", lw=2, label="compound: x1.05 each month")
ax[0].set_xlabel("month"); ax[0].set_ylabel("monthly users"); ax[0].set_title("Simple vs compound growth")
ax[0].legend(fontsize=8, loc="upper left"); ax[0].grid(alpha=.3)
labels = ["start", "-20%", "then +20%", "then +25%"]
vals = [100, 80, 96, 100]
cols = ["#357a70", "#aa2d26", "#6a2fd0", "#357a70"]
ax[1].bar(labels, vals, color=cols)
for i, v in enumerate(vals): ax[1].text(i, v + 1.5, str(v), ha="center")
ax[1].set_ylim(0, 118); ax[1].set_title("A 20% drop needs a 25% rise"); ax[1].set_ylabel("price")
plt.tight_layout(); plt.savefig("ch01_growth.png", dpi=110)
