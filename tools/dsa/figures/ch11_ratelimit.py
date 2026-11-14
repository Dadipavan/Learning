import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
txt(ax, 8, 7.9, "Sliding-window rate limiter: 3 requests per 10 seconds", BLUE, 16, weight="bold")
ax.plot([0.8, 15.2], [3.2, 3.2], color="black", lw=2.5, zorder=2)


def X(t):
    return 0.8 + t * 0.95


for t in range(0, 15):
    ax.plot([X(t)] * 2, [3.0, 3.4], color="black", lw=1.5)
    txt(ax, X(t), 2.5, str(t), GREY, 12)
for t, ok in ((1, 1), (3, 1), (4, 1), (8, 0), (12, 1), (13, 1)):
    c = TEAL if ok else RED
    ax.scatter([X(t)], [3.2], s=420, color=c, zorder=5)
    txt(ax, X(t), 4.1, "ok" if ok else "deny", c, 13, weight="bold")
ax.add_patch(Rectangle((X(3.5), 5.0), X(13.3) - X(3.5), 0.7, fc="#dbe3fb", ec=BLUE, lw=2, zorder=1))
txt(ax, (X(3.5) + X(13.3)) / 2, 5.35, "window at t = 13 covers times 4 to 13", BLUE, 13)
txt(ax, 8, 1.2, "deque after t = 13 holds [4, 12, 13]", ORANGE, 14)
save(fig, "dsa11_ratelimit.png")
