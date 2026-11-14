import sys, os, random, statistics
sys.path.insert(0, "/Users/c2487352/Personal/Career/final/tools/figs_de")
from common import *
random.seed(5)
def sim(lam, mu, n=60000):
    t = 0; free = 0; w = []
    for _ in range(n):
        t += random.expovariate(lam); s = max(t, free); free = s + random.expovariate(mu); w.append(free - t)
    w.sort(); return statistics.mean(w) * 1000, w[int(.95*n)] * 1000, w[int(.99*n)] * 1000
rhos = [0.3, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95]
res = [sim(r * 100, 100) for r in rhos]
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(rhos, [r[0] for r in res], "o-", color=BLUE, label="mean")
ax.plot(rhos, [r[1] for r in res], "s-", color=ORANGE, label="p95")
ax.plot(rhos, [r[2] for r in res], "^-", color=RED, label="p99")
ax.axhline(200, color=GREY, ls="--"); ax.text(0.31, 210, "latency target 200 ms", color=GREY, fontsize=9)
ax.set_xlabel("utilization (arrival rate / service rate)"); ax.set_ylabel("latency (ms)")
ax.set_title("Latency explodes as a single consumer approaches full load"); ax.legend(); ax.grid(alpha=.3)
fig.savefig("de_latency_curve.png", dpi=110, bbox_inches="tight")
