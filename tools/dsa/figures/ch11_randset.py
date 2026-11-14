import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
txt(ax, 8, 7.9, "Random set: remove 20 by swapping with the last item", BLUE, 16, weight="bold")


def row(y, items, col, label):
    txt(ax, 1.1, y + 0.6, label, GREY, 13)
    for i, v in enumerate(items):
        box(ax, 2.6 + i * 2.4, y, 2.2, 1.2, str(v), col, fs=16)
        txt(ax, 3.7 + i * 2.4, y - 0.35, str(i), GREY, 11)


row(4.6, [10, 20, 30, 40], BLUE, "before")
row(2.0, [10, 40, 30], TEAL, "after")
arrow(ax, (10.9, 5.9), (6.1, 5.9), RED, 3, rad=-0.5)
txt(ax, 8.5, 7.1, "1. copy last (40) over the 20", RED, 13)
txt(ax, 12.8, 2.6, "2. pop the last slot\n(4 slots become 3)", ORANGE, 13)
txt(ax, 8.0, 0.7, "3. fix dict: 40 now at index 1, delete key 20", PURPLE, 13)
save(fig, "dsa11_randset.png")
