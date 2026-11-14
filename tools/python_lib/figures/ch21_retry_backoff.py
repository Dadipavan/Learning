import matplotlib
matplotlib.use("Agg")
import random
import numpy as np
import matplotlib.pyplot as plt
base, cap = 0.5, 8.0
att = np.arange(7)
ceil = np.minimum(cap, base * 2.0 ** att)
rng = random.Random(1)
plt.rcParams.update({"font.size": 12})
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.bar(att, ceil, color="#2b4fd6", alpha=0.85, label="max wait: min(cap, 0.5 x 2^attempt)")
for k in range(8):
    ys = [rng.uniform(0, c) for c in ceil]
    ax.scatter(att + (k - 3.5) * 0.07, ys, color="#b84a22", s=26, zorder=3, label="jittered wait (one dot per client)" if k == 0 else None)
ax.axhline(cap, color="#aa2d26", ls="--", lw=1.8, label="cap = 8 s")
ax.set_xlabel("retry attempt number"); ax.set_ylabel("seconds waited")
ax.legend(fontsize=10, loc="upper left"); ax.grid(alpha=0.25, axis="y")
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig("lib21_retry_backoff.png", dpi=110)
