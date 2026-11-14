import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
txt(ax, 8.0, 7.8, 'Checking  { [ ( ) ] }  with a stack', BLUE, 15, weight="bold")
snaps = [("read  {  [  (", ["{", "[", "("]),
         ("read  )  : pop (", ["{", "["]),
         ("read  ]  : pop [", ["{"]),
         ("read  }  : pop {", [])]
for k, (title, st) in enumerate(snaps):
    x0 = 0.8 + k * 3.9
    txt(ax, x0 + 1.4, 6.6, title, GREY, 12)
    ax.plot([x0, x0, x0 + 2.8, x0 + 2.8], [5.9, 0.8, 0.8, 5.9], color="black", lw=3, zorder=2)
    for i, c in enumerate(st):
        box(ax, x0 + 0.2, 0.95 + i * 1.3, 2.4, 1.2, c, [BLUE, ORANGE, TEAL][i], fs=18)
    if st:
        txt(ax, x0 + 1.4, 1.0 + len(st) * 1.3 + 0.35, "top", RED, 12)
    else:
        txt(ax, x0 + 1.4, 2.3, "empty:\nvalid", TEAL, 13, weight="bold")
save(fig, "dsa5_stack.png")
