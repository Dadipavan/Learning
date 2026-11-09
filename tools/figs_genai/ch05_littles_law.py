import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
lat = np.linspace(0.5, 12, 100)
fig, ax = plt.subplots(figsize=(8, 4.2))
for r, c in [(5, "#357a70"), (10, "#2b4fd6"), (20, "#b84a22")]:
    ax.plot(lat, r * lat, color=c, lw=2, label=f"{r} requests/s")
ax.axhline(100, color="#aa2d26", ls="--"); ax.text(0.7, 104, "provider limit: 100 in flight", color="#aa2d26", fontsize=9)
ax.scatter([6], [120], color="#b84a22", zorder=5); ax.annotate("20/s at 6 s = 120\n(over the limit)", (6, 120), (7.2, 150), fontsize=8, arrowprops=dict(arrowstyle="->"))
ax.scatter([4], [80], color="#357a70", zorder=5); ax.annotate("shorter output: 4 s = 80", (4, 80), (0.8, 55), fontsize=8, arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("average latency (s)"); ax.set_ylabel("requests in flight = rate x latency")
ax.set_title("Little's Law: concurrency you must support", fontsize=10)
ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0, 0.9)); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch05d_littles_law.png", dpi=110)
