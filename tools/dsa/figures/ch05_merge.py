import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
def row(vals, y, color, name, x0=3.0):
    txt(ax, 0.2, y + 0.55, name, color, 14, "left", weight="bold")
    for i, v in enumerate(vals):
        x = x0 + i * 2.6
        box(ax, x, y, 1.4, 1.1, str(v), color)
        if i < len(vals) - 1:
            arrow(ax, (x + 1.42, y + 0.55), (x + 2.58, y + 0.55), GREY, ms=13)
    return x0
row([1, 4, 6], 6.6, BLUE, "a")
row([2, 3, 7], 4.4, ORANGE, "b")
# result
y = 1.0
txt(ax, 0.2, y + 0.55, "out", TEAL, 14, "left", weight="bold")
res = ["dummy", 1, 2, 3, 4]
for i, v in enumerate(res):
    x = 1.5 + i * 2.6
    box(ax, x, y, 1.6 if i == 0 else 1.4, 1.1, str(v), TEAL, fc="#eeeeee" if i == 0 else "white", fs=12 if i == 0 else 15)
    if i < len(res) - 1:
        arrow(ax, (x + 1.62, y + 0.55), (x + 2.58, y + 0.55), GREY, ms=13)
txt(ax, 1.5 + 4 * 2.6 + 0.7, y + 1.6, "tail", PURPLE, 13)
arrow(ax, (1.5 + 4 * 2.6 + 0.7, y + 1.35), (1.5 + 4 * 2.6 + 0.7, y + 1.12), PURPLE, ms=12)
txt(ax, 13.5, 4.9, "pick the smaller\nfront, hook it\nonto tail", GREY, 12)
save(fig, "dsa5_merge.png")
