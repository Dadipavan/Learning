import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
labels = ["dummy", "1", "2", "3", "4", "5"]
xs = [0.6 + i * 2.55 for i in range(6)]
y = 3.2
for i, (x, l) in enumerate(zip(xs, labels)):
    box(ax, x, y, 1.6, 1.3, l, BLUE if i else GREY, fc="#eeeeee" if i == 0 else "white", fs=14)
    if i < 5:
        arrow(ax, (x + 1.62, y + 0.65), (xs[i + 1] - 0.02, y + 0.65), GREY)
txt(ax, xs[5] + 2.3, y + 0.65, "None", RED, 13)
# n = 2: remove "4". slow ends at 3 (index 3), fast ends at None
txt(ax, xs[3] + 0.8, y - 0.9, "slow", TEAL, 15, weight="bold")
arrow(ax, (xs[3] + 0.8, y - 0.55), (xs[3] + 0.8, y - 0.03), TEAL)
txt(ax, xs[5] + 0.8, y - 0.9, "fast", ORANGE, 15, weight="bold")
arrow(ax, (xs[5] + 0.8, y - 0.55), (xs[5] + 0.8, y - 0.03), ORANGE)
box(ax, xs[4], y, 1.6, 1.3, '4', RED, fc='#f6dcd9', fs=14)
txt(ax, xs[4] + 0.8, y - 0.9, 'removed', RED, 13)
arrow(ax, (xs[3] + 0.8, y + 1.35), (xs[5] + 0.8, y + 1.35), PURPLE, rad=-0.35)
txt(ax, (xs[3] + xs[5]) / 2 + 0.8, y + 3.0, "slow.next = slow.next.next", PURPLE, 13)
txt(ax, 8.0, 7.6, "Remove the 2nd node from the end (n = 2)", BLUE, 15, weight="bold")
txt(ax, 8.0, 0.8, "fast starts n steps ahead; when fast reaches None, slow sits just before the target", GREY, 11)
save(fig, "dsa5_remove_nth.png")
