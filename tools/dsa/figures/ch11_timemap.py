import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
txt(ax, 8, 7.9, "Time-based store: latest value at or before t", BLUE, 16, weight="bold")
ts = [1, 4, 9, 12]
vals = ["a", "b", "c", "d"]
txt(ax, 1.2, 5.6, "times", GREY, 13)
txt(ax, 1.2, 4.0, "values", GREY, 13)
for i, (t, v) in enumerate(zip(ts, vals)):
    x = 3.0 + i * 3.0
    box(ax, x, 5.0, 2.2, 1.2, str(t), BLUE, fs=16)
    box(ax, x, 3.4, 2.2, 1.2, v, TEAL, fs=16)
    txt(ax, x + 1.1, 6.6, "idx %d" % i, GREY, 12)
arrow(ax, (7.1, 2.1), (7.1, 3.3), ORANGE, 3)
txt(ax, 7.1, 1.7, "query t = 6 lands between 4 and 9", ORANGE, 12)
txt(ax, 8.0, 0.7, "bisect_right(times, 6) = 2, so answer index = 2 - 1 = 1, value b", ORANGE, 13)
save(fig, "dsa11_timemap.png")
