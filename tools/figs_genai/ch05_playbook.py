import sys, os
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
from ch05_boxes import *
fig, ax = canvas(8, 4.6)
ax.set_title("Playbook: classify the problem first", fontsize=11)
box(ax, 36, 86, 28, 11, "What is the symptom?", BLUE)
items = [
 (1, "Errors / flaky\n(429, 5xx, hangs)", ORANGE, "Pattern A, B\nclassify, backoff,\ntimeouts, budget"),
 (21, "Slow answers", PURPLE, "Pattern C\nTTFT vs total,\nshorten output"),
 (41, "Bill too high", RED, "Pattern D, E\ntokens x price,\ncache, history"),
 (61, "Capacity /\nthrottling", TEAL, "Pattern F\nLittle's Law,\ntoken bucket"),
 (81, "Wrong user data,\nleaked key", "#444444", "Pattern G\ncache key,\nrotate, redact"),
]
for x, s, c, a in items:
    arrow(ax, 50, 85, x + 9, 66, "#444444")
    box(ax, x, 48, 18, 17, s, c, fs=7.5)
    arrow(ax, x + 9, 47, x + 9, 36, c)
    box(ax, x, 12, 18, 23, a, c, fs=7.5)
ax.text(50, 4, "Then: write the formula or the log line that proves it, fix one thing, measure again.", ha="center", fontsize=8, color="#444444")
ax.set_ylim(1, 100)
fig.tight_layout(); fig.savefig("ch05d_playbook.png", dpi=110)
