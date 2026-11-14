from common import *
fig, ax = canvas(8.5, 4.2)
ax.set_xlim(0, 11); ax.set_ylim(0, 5.4)
ax.text(0.1, 5.1, "Lost update: two threads run  counter += 1  with no lock", fontsize=11, fontweight="bold")
ax.text(1.6, 4.5, "Thread 1", ha="center", color=BLUE, fontweight="bold"); ax.text(5.2, 4.5, "Thread 2", ha="center", color=ORANGE, fontweight="bold")
ax.text(9.2, 4.5, "counter", ha="center", color=GREY, fontweight="bold")
rows = [("read counter -> 5", None, "5"), (None, "read counter -> 5", "5"), ("write 5 + 1 = 6", None, "6"), (None, "write 5 + 1 = 6", "6  (should be 7)")]
for i, (a, b, c) in enumerate(rows):
    y = 3.5 - i * 0.9
    if a: box(ax, 0.2, y, 2.8, 0.65, a, BLUE, fs=10)
    if b: box(ax, 3.8, y, 2.8, 0.65, b, ORANGE, fs=10)
    box(ax, 8.0, y, 2.4, 0.65, c, RED if "should" in c else GREY, fs=10)
ax.text(0.2, 0.1, "Fix: hold a threading.Lock around read-modify-write so only one thread is inside at a time.", fontsize=10, color=TEAL)
save(fig, "ch11_lost_update.png")
