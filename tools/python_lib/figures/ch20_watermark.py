import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

runs = ["run 1", "run 2", "run 3", "run 4", "run 5"]
new_rows = [1000, 120, 95, 0, 140]
cum = np.cumsum(new_rows)
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.bar(runs, new_rows, color=B, label="rows loaded this run")
ax.set_ylabel("rows loaded this run")
ax2 = ax.twinx(); ax2.spines["right"].set_visible(True)
ax2.plot(runs, cum, "-o", color=O, lw=2.5, label="rows in target table")
ax2.set_ylabel("rows in target table")
for r, c, n in zip(runs, cum, new_rows):
    ax2.text(r, c + 40, f"total {c}", ha="center", fontsize=10, color=O, bbox=dict(fc="white", ec="none", alpha=0.85, pad=1))
ax.set_title("Watermark: each run loads only rows newer than the last mark")
ax.set_ylim(0, 1250); ax2.set_ylim(0, 1700)
fig.tight_layout(); fig.savefig("lib20_watermark.png")
