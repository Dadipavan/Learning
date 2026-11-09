import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
txt(ax, 8, 7.9, "Queue from two stacks: enqueue 1, 2, 3, then dequeue", BLUE, 16, weight="bold")
for x0, title, data, col, note in ((1.5, "in_stack", [1, 2, 3], BLUE, "push goes here, top = 3"),
                                   (10.0, "out_stack", [3, 2, 1], TEAL, "pop comes from here\ntop = 1 = queue front")):
    txt(ax, x0 + 2.0, 7.0, title, col, 14, weight="bold")
    ax.plot([x0, x0, x0 + 4.0, x0 + 4.0], [6.4, 1.6, 1.6, 6.4], color="black", lw=3, zorder=2)
    for i, v in enumerate(data):
        box(ax, x0 + 0.3, 1.8 + i * 1.3, 3.4, 1.1, str(v), col, fs=16)
    txt(ax, x0 + 2.0, 0.7, note, GREY, 12)
arrow(ax, (6.0, 4.0), (9.7, 4.0), RED, 3)
txt(ax, 7.85, 5.2, "only when out_stack\nis empty: pop all\nfrom in, push to out", RED, 12)
save(fig, "dsa11_twostacks.png")
