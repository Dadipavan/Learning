import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_boxes import *
fig, ax = canvas()
ax.set_title("Which failures do you retry?", fontsize=11)
box(ax, 38, 84, 24, 12, "The call failed.\nWhat was it?", BLUE)
cols = [
 (1, "400 bad request\ncontext too long\n(your input is wrong)", RED, "Fix the request.\nDo NOT retry.", "FAIL FAST"),
 (26, "401 / 403\nbad or missing key,\nno permission", RED, "Fix the key or access.\nDo NOT retry.", "FAIL FAST"),
 (51, "429 rate limit\n(honour Retry-After)", ORANGE, "Wait, then retry\nwith backoff + jitter.", "RETRY"),
 (76, "500 / 502 / 503\ntimeout, dropped\nconnection", ORANGE, "Retry with backoff.\nCheck idempotency.", "RETRY"),
]
for x, t, c, a, tag in cols:
    arrow(ax, 50, 83, x + 11, 66, "#444444")
    box(ax, x, 48, 22, 17, t, c, fs=8)
    arrow(ax, x + 11, 47, x + 11, 33, c)
    box(ax, x, 16, 22, 16, a, c, fs=8)
    ax.text(x + 11, 8, tag, ha="center", fontsize=9, color=c, fontweight="bold")
ax.text(50, 0, "After the retry budget is spent (for example 4 retries or 60 s) stop and raise a clear error.",
        ha="center", fontsize=8, color="#444444")
ax.set_ylim(-4, 100)
fig.tight_layout(); fig.savefig("ch05d_error_tree.png", dpi=110)
