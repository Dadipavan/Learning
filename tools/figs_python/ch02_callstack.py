from common import *
fig, ax = canvas(8, 4.4)
ax.set_xlim(0, 10); ax.set_ylim(0, 5.6)
frames = [("factorial(1)  n=1  returns 1", TEAL), ("factorial(2)  n=2  waits: 2 * ?", BLUE),
          ("factorial(3)  n=3  waits: 3 * ?", BLUE), ("factorial(4)  n=4  waits: 4 * ?", BLUE),
          ("module level: print(factorial(4))", GREY)]
for i, (t, c) in enumerate(frames):
    box(ax, 0.3, 0.3 + i * 1.0, 5.6, 0.8, t, c, fs=10.5)
ax.text(0.3, 5.4, "Call stack at the deepest point (top = newest)", fontsize=11, fontweight="bold")
arrow(ax, 6.3, 4.3, 6.3, 0.8, GREY)
ax.text(6.5, 3.2, "return values flow\nback down:\n1, then 2*1=2,\nthen 3*2=6,\nthen 4*6=24", fontsize=10.5, va="center")
save(fig, "ch02_callstack.png")
