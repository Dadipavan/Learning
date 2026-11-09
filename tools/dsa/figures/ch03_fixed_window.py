from ch03_common import *
a = [2, 1, 5, 1, 3, 2, 9, 1]
k = 3
fig, ax = new_fig()
notes = ["sum = 2 + 1 + 5 = 8", "7 = 8 - 2 (out) + 1 (in)", "9 = 7 - 1 (out) + 3 (in)"]
for s in range(3):
    y = -s * 2.5
    draw_array(ax, a, y=y, fills={i: BLUE for i in range(s, s + k)}, idx=False)
    ax.add_patch(Rectangle((s, y), k, 1, fc="none", ec=BLUE, lw=4))
    ax.text(8.4, y + 0.5, notes[s], va="center", fontsize=14, color=BLUE)
    if s:
        ax.text(s - 0.5, y + 1.15, "out", ha="center", fontsize=12, color=RED)
        ax.text(s + k - 0.5, y + 1.15, "in", ha="center", fontsize=12, color=TEAL)
ax.set_xlim(-0.3, 15.5); ax.set_ylim(-5.4, 2)
ax.set_title("Fixed window of size 3: slide by one, update the sum", fontsize=15)
save(fig, "dsa3_fixed_window.png")
