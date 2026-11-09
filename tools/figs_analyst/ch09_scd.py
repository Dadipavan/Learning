import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
cities = ["Delhi", "Mumbai", "Pune"]; t1 = [400, 600, 0]; t2 = [400, 300, 300]
x = np.arange(3); w = 0.36
fig, ax = plt.subplots(figsize=(8, 3.8), dpi=110)
b1 = ax.bar(x - w/2, t1, w, color="#aa2d26", label="Type 1 (overwrite): history lost")
b2 = ax.bar(x + w/2, t2, w, color="#357a70", label="Type 2 (history rows): city at time of sale")
for bars in (b1, b2):
    for b in bars: ax.text(b.get_x() + b.get_width()/2, b.get_height() + 12, f"{b.get_height():.0f}", ha="center", fontsize=11)
ax.set_xticks(x); ax.set_xticklabels(cities, fontsize=11); ax.set_ylabel("revenue (Rs)", fontsize=11); ax.set_ylim(0, 720)
ax.legend(frameon=False, fontsize=9, loc="upper left")
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch09_scd.png")
