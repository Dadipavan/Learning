import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import numpy as np
from scipy import stats
za = stats.norm.ppf(0.975)
def power(p1, p2, n):
    pb = (p1 + p2) / 2
    se0 = np.sqrt(2 * pb * (1 - pb) / n); se1 = np.sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / n)
    return stats.norm.cdf((abs(p2 - p1) - za * se0) / se1)
n = np.arange(500, 40001, 250)
fig, ax = plt.subplots(figsize=(8, 4.2))
for d, c in [(0.005, ORANGE), (0.01, BLUE), (0.02, TEAL)]:
    ax.plot(n, power(0.10, 0.10 + d, n), color=c, lw=2, label=f"lift {d*100:.1f} point(s)")
ax.axhline(0.8, color=GREY, ls="--"); ax.text(30500, 0.82, "80% power", color=GREY)
ax.set_xlabel("customers per arm"); ax.set_ylabel("power (chance to detect a real lift)")
ax.set_title("Power rises with sample size and falls as the lift shrinks (baseline 10%)"); ax.legend(loc="lower right")
save("ds_ch07_power_curve.png")
# sequential boundaries
k = np.arange(1, 6)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(k, [1.96] * 5, "o--", color=RED, lw=2, label="naive: 1.96 at every look (false alarm about 14%)")
ax.plot(k, [2.413] * 5, "s-", color=BLUE, lw=2, label="Pocock: 2.413 at every look (about 5%)")
ax.plot(k, 2.04 * np.sqrt(5 / k), "^-", color=TEAL, lw=2, label="O'Brien-Fleming style (about 5%)")
ax.set_xticks(k); ax.set_xlabel("look number (equally spaced)"); ax.set_ylabel("|z| needed to stop and declare a win")
ax.set_title("Looking five times: how strict each look must be"); ax.legend(fontsize=9)
save("ds_ch07_boundaries.png")
