import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd, os, tempfile, tracemalloc
BL, OR, TE, RE, PU = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 13, "axes.titlesize": 15})

rng = np.random.default_rng(3)
fig, axs = plt.subplots(1, 2, figsize=(8, 4.2), sharex=True)
even = rng.normal(10, 1.2, 40).clip(6, 14)
skew = np.append(rng.normal(10, 1.2, 39).clip(6, 14), 55.0)
for ax, d, t, c in zip(axs, [even, skew], ["Healthy stage", "Skewed stage"], [TE, RE]):
    ax.bar(np.arange(len(d)), d, color=c); ax.set_title(t); ax.set_xlabel("task id")
    ax.axhline(np.median(d), color="#333", ls="--", lw=2); ax.text(1, np.median(d) + 1.5, "median %.0f s" % np.median(d), fontsize=11)
    ax.text(len(d) - 3, d.max() * 0.93, "max %.0f s" % d.max(), ha="right", fontsize=11)
axs[0].set_ylabel("task duration (s), simulated")
fig.tight_layout(); fig.savefig("lib22_sparkui.png", dpi=110)
