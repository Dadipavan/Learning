import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 9.4, (8, 4.7))
# states: (next array as target index or None, prev idx, curr idx, title)
states = [
    ([1, 2, 3, None], None, 0, "start"),
    ([None, 2, 3, None], 0, 1, "after step 1"),
    ([None, 0, 3, None], 1, 2, "after step 2"),
    ([None, 0, 1, 2], 3, None, "done: prev is the new head"),
]
vals = [1, 2, 3, 4]
for r, (nxt, prev, curr, title) in enumerate(states):
    y = 7.4 - r * 2.0
    txt(ax, 0.2, y + 0.55, title, GREY, 11, "left")
    xs = [5.0 + i * 2.6 for i in range(4)]
    for i, x in enumerate(xs):
        box(ax, x, y, 1.3, 1.1, str(vals[i]), BLUE, fs=15)
    for i, t in enumerate(nxt):
        x = xs[i]
        if t is None:
            arrow(ax, (x + 0.65, y), (x + 0.65, y - 0.4), RED, ms=12)
            txt(ax, x + 1.25, y - 0.3, 'None', RED, 10, 'left')
        elif t > i:
            arrow(ax, (x + 1.3, y + 0.55), (xs[t] - 0.02, y + 0.55), GREY)
        else:
            arrow(ax, (x, y + 0.55), (xs[t] + 1.32, y + 0.55), TEAL)
    if prev is not None:
        txt(ax, xs[prev] + 0.65, y + 1.5, "prev", ORANGE, 12)
    if curr is not None:
        txt(ax, xs[curr] + 0.65, y + 1.5 if curr != prev else y + 1.9, "curr", PURPLE, 12)
save(fig, "dsa5_reverse.png")
