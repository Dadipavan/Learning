from ch12_common import *
import numpy as np
days = [0, 1, 3, 7, 14, 30]
fig, ax = plt.subplots(figsize=(8, 4.2))
x = np.linspace(0, 45, 600); y = np.zeros_like(x)
last = 0.0; strength = 1.5
for i, xv in enumerate(x):
    if any(abs(xv - d) < 0.04 for d in days) and xv > last + 0.2:
        last = xv; strength *= 1.9
    y[i] = np.exp(-(xv - last) / strength)
ax.plot(x, y, color=B, lw=3)
for k, d in enumerate(days):
    ax.axvline(d, color=O, lw=2, ls="--")
    ax.text(d, 1.07 + (0.07 if k == 1 else 0), "R%d" % k if k else "solve", ha="right" if k == 0 else "center", color=O, fontsize=13, fontweight="bold")
ax.set_ylim(0, 1.2); ax.set_xlim(-1, 45)
ax.set_xlabel("days since first solving the problem", fontsize=14); ax.set_ylabel("chance you recall it", fontsize=14)
ax.set_title("Illustrative sketch (not measured data): each review slows forgetting", fontsize=13)
plt.tight_layout(); plt.savefig("dsa12_spaced.png", dpi=110)
