from ch03_common import *
orig = [1, 1, 2, 2, 2, 3, 4, 4]
now = [1, 2, 3, 2, 2, 3, 4, 4]
w, r = 3, 6
fig, ax = new_fig()
draw_array(ax, orig, y=3.4, idx=False, fs=16)
ax.text(-0.3, 3.9, "start", ha="right", va="center", fontsize=14)
fills = {i: TEAL for i in range(w)}
fills.update({i: "#cccccc" for i in range(w, r)})
from ch03_common import LIGHT
LIGHT["#cccccc"] = "#e3e3e3"
draw_array(ax, now, y=0, fills=fills, idx=True)
ax.text(-0.3, 0.5, "now", ha="right", va="center", fontsize=14)
pointer(ax, w, 0, "w (write)", BLUE, length=0.6, fs=14)
pointer(ax, r, 0, "r (read)", ORANGE, length=0.6, fs=14)
ax.text(1.5, 1.25, "kept", ha="center", fontsize=13, color=TEAL)
ax.text(4.5, 1.25, "read, junk", ha="center", fontsize=13, color="#777777")
ax.text(6.9, 1.25, "unread", ha="center", fontsize=13, color="#222222")
ax.set_xlim(-2.2, 8.5); ax.set_ylim(-3, 5.3)
ax.set_title("Reader and writer: remove duplicates, about to read index 6", fontsize=15)
save(fig, "dsa3_reader_writer.png")
