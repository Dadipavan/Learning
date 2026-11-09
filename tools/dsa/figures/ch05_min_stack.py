import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
txt(ax, 8.0, 7.8, "Min stack: push 5, 3, 7, 3, 8", BLUE, 15, weight="bold")
vals = [5, 3, 7, 3, 8]
mins = [5, 3, 3, 3, 3]
for x0, title, data, col in ((2.0, "values stack", vals, BLUE), (9.0, "min stack", mins, TEAL)):
    txt(ax, x0 + 2.0, 6.9, title, col, 14, weight="bold")
    ax.plot([x0, x0, x0 + 4.0, x0 + 4.0], [6.3, 0.5, 0.5, 6.3], color="black", lw=3, zorder=2)
    for i, v in enumerate(data):
        box(ax, x0 + 0.3, 0.7 + i * 1.1, 3.4, 1.0, str(v), col, fs=16)
txt(ax, 7.0, 3.6, "same\nheight", GREY, 12)
txt(ax, 14.9, 5.6, "top =\nminimum", RED, 12)
save(fig, "dsa5_min_stack.png")
