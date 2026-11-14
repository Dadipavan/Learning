import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas()
txt(ax, 1.0, 7.6, "Singly linked list", BLUE, 15, "left", weight="bold")
txt(ax, 0.8, 6.3, "head", ORANGE, 14)
arrow(ax, (1.5, 6.3), (2.6, 6.3), ORANGE)
vals = [3, 7, 9]
for i, v in enumerate(vals):
    x = 2.7 + i * 4.2
    box(ax, x, 5.7, 1.5, 1.2, str(v), BLUE)
    box(ax, x + 1.5, 5.7, 1.0, 1.2, "", BLUE, fc="#e8edfb")
    if i < 2:
        arrow(ax, (x + 2.0, 6.3), (x + 4.2, 6.3), GREY)
    else:
        arrow(ax, (x + 2.0, 6.3), (x + 3.2, 6.3), GREY)
        txt(ax, x + 4.0, 6.3, "None", RED, 14)
txt(ax, 4.0, 4.9, "value | next", GREY, 12)

txt(ax, 1.0, 3.7, "Doubly linked list", TEAL, 15, "left", weight="bold")
for i, v in enumerate(vals):
    x = 2.0 + i * 4.6
    box(ax, x, 1.4, 1.0, 1.2, "", TEAL, fc="#e3f1ee")
    box(ax, x + 1.0, 1.4, 1.5, 1.2, str(v), TEAL)
    box(ax, x + 2.5, 1.4, 1.0, 1.2, "", TEAL, fc="#e3f1ee")
    if i < 2:
        arrow(ax, (x + 3.0, 2.2), (x + 4.6 + 0.5, 2.2), GREY, rad=0)
        arrow(ax, (x + 4.6 + 0.5, 1.8), (x + 3.0, 1.8), ORANGE, rad=0)
txt(ax, 3.5, 0.6, "prev | value | next", GREY, 12)
save(fig, "dsa5_list_nodes.png")
