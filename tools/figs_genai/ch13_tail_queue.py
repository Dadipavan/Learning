"""Two panels: latency percentiles on a skewed sample, and wait time vs utilisation (M/M/1). Saves ch13_tail_queue.png."""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
plt.rcParams.update({"font.size": 11})
lat = [0.8, 0.9, 0.9, 1.0, 1.0, 1.1, 1.1, 1.2, 1.2, 1.3, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0, 2.4, 3.1, 6.2, 12.5]
fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 4.2))
a.bar(range(1, 21), lat, color=BLUE)
for y, name, c in [(np.mean(lat), "mean 2.2 s", TEAL), (1.3, "p50 1.3 s", PURPLE), (6.2, "p95 6.2 s", ORANGE)]:
    a.axhline(y, color=c, lw=2, ls="--"); a.text(0.6, y + 0.25, name, color=c, fontsize=10, fontweight="bold")
a.set_xlabel("request (sorted by latency)"); a.set_ylabel("latency (seconds)"); a.set_title("20 requests: the tail drives p95")
rho = np.linspace(0.05, 0.97, 200)
mu = 2.0
b.plot(rho, 1 / (mu * (1 - rho)), color=RED, lw=2.5)
for r in (0.5, 0.8, 0.9, 0.95):
    w = 1 / (mu * (1 - r)); b.plot([r], [w], "o", color=BLUE); b.annotate("%.0f%%: %.1f s" % (r * 100, w), (r, w), textcoords="offset points", xytext=(-62, 4), fontsize=10)
b.set_xlabel("utilisation (arrival rate / capacity)"); b.set_ylabel("average time in system (s)"); b.set_title("Waiting explodes near full load")
b.set_ylim(0, 12)
for ax in (a, b): ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch13_tail_queue.png", dpi=110)
