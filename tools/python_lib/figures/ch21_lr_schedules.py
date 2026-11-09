import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 12})
s = np.arange(0, 1001)
const = np.full_like(s, 3e-4, dtype=float)
step = 3e-4 * 0.1 ** (s // 400)
cos = 0.5 * 3e-4 * (1 + np.cos(np.pi * s / 1000))
warm = np.where(s < 100, 3e-4 * s / 100, 0.5 * 3e-4 * (1 + np.cos(np.pi * (s - 100) / 900)))
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(s, const, color=B, lw=2.5, label="constant")
ax.plot(s, step, color=O, lw=2.5, label="step decay (x0.1 every 400)")
ax.plot(s, cos, color=T, lw=2.5, label="cosine")
ax.plot(s, warm, color=P, lw=3, label="warm-up 100 + cosine")
ax.set_xlabel("training step"); ax.set_ylabel("learning rate")
ax.legend(fontsize=11, loc="upper right"); ax.grid(alpha=0.25)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig("lib21_lr_schedules.png", dpi=110)
