import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
txt(ax, 8.0, 7.9, "Queue: first in, first out", BLUE, 15, weight="bold")
vals = ["D", "C", "B", "A"]
for i, v in enumerate(vals):
    box(ax, 4.0 + i * 2.2, 5.6, 2.0, 1.4, v, BLUE, fs=17)
arrow(ax, (1.0, 6.3), (3.8, 6.3), RED)
txt(ax, 2.4, 7.0, "enqueue (back)", RED, 12)
arrow(ax, (12.9, 6.3), (15.6, 6.3), TEAL)
txt(ax, 14.3, 7.0, "dequeue (front)", TEAL, 12)
txt(ax, 5.0, 5.1, "back", GREY, 12); txt(ax, 11.8, 5.1, "front", GREY, 12)
txt(ax, 8.0, 4.0, "Deque: both ends open", PURPLE, 15, weight="bold")
for i, v in enumerate(["7", "9", "4"]):
    box(ax, 5.2 + i * 2.2, 1.6, 2.0, 1.4, v, PURPLE, fs=17)
arrow(ax, (1.2, 2.5), (5.0, 2.5), ORANGE, style="<|-|>")
txt(ax, 3.0, 3.3, "appendleft / popleft", ORANGE, 12)
arrow(ax, (12.0, 2.5), (15.2, 2.5), ORANGE, style="<|-|>")
txt(ax, 13.6, 3.3, "append / pop", ORANGE, 12)
save(fig, "dsa5_queue_deque.png")
