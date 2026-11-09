import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

a = [1, 3, -1, -3, 5, 3, 6, 7]
fig, ax = canvas(16, 8.4)
txt(ax, 8.0, 7.9, "Sliding window maximum, k = 3", BLUE, 15, weight="bold")
for i, v in enumerate(a):
    box(ax, 1.0 + i * 1.8, 5.4, 1.6, 1.3, str(v), BLUE, fs=16)
    txt(ax, 1.8 + i * 1.8, 5.0, str(i), GREY, 11)
# first window [0..2]
ax.add_patch(Rectangle((0.9, 5.3), 5.4, 1.5, fc="none", ec=ORANGE, lw=4, zorder=5))
txt(ax, 3.7, 7.2, "window 1: max 3", ORANGE, 12)
ax.add_patch(Rectangle((0.9 + 4 * 1.8, 5.3), 5.4, 1.5, fc="none", ec=TEAL, lw=4, zorder=5, ls="--"))
txt(ax, 3.7 + 7.2, 7.2, "window 5: max 6", TEAL, 12)
txt(ax, 1.3, 3.7, "answer", GREY, 13, "left")
for i, v in enumerate([3, 3, 5, 5, 6, 7]):
    box(ax, 3.2 + i * 1.8, 3.2, 1.6, 1.0, str(v), TEAL, fs=15)
txt(ax, 1.3, 1.6, "deque holds indexes of a decreasing run, front = max", PURPLE, 12, "left")
txt(ax, 1.3, 0.8, "(window 5 covers indexes 4 to 6: values 5, 3, 6)", GREY, 11, "left")
save(fig, "dsa5_window_max.png")
