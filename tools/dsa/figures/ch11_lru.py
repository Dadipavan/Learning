import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
txt(ax, 8, 7.9, "LRU cache: hash map + doubly linked list", BLUE, 16, weight="bold")
txt(ax, 4.8, 6.8, "most recent", TEAL, 13)
txt(ax, 12.4, 6.8, "least recent (evict me)", RED, 13)
xs = [0.3, 3.5, 6.7, 9.9, 13.3]
names = ["HEAD", "c : 3", "a : 1", "b : 2", "TAIL"]
cols = [GREY, BLUE, BLUE, BLUE, GREY]
ws = [2.2, 2.6, 2.6, 2.6, 2.2]
for x, n, c, w in zip(xs, names, cols, ws):
    box(ax, x, 4.3, w, 1.5, n, c, fs=15)
for i in range(4):
    x0 = xs[i] + ws[i]
    x1 = xs[i + 1]
    arrow(ax, (x0, 5.3), (x1, 5.3), TEAL, 2)
    arrow(ax, (x1, 4.8), (x0, 4.8), ORANGE, 2)
txt(ax, 8, 0.25, "teal = next, orange = prev (two-way, so removing a node is O(1))", GREY, 12)
for key, x in (("c", 3.5), ("a", 6.7), ("b", 9.9)):
    box(ax, x + 0.3, 0.7, 2.0, 1.2, "'%s'" % key, PURPLE, fs=15)
    arrow(ax, (x + 1.3, 1.9), (x + 1.3, 4.25), PURPLE, 2)
txt(ax, 1.5, 1.3, "dict:\nkey to node", PURPLE, 13)
save(fig, "dsa11_lru.png")
