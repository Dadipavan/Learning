from ch03_common import *
vals = [1, 3, 4, 6, 8, 11, 15]
steps = [(0, 6, "1 + 15 = 16 > 14, too big: move R left"),
         (0, 5, "1 + 11 = 12 < 14, too small: move L right"),
         (1, 5, "3 + 11 = 14, found it")]
fig, ax = new_fig()
for k, (l, r, msg) in enumerate(steps):
    y = -k * 3.3
    draw_array(ax, vals, y=y, fills={l: BLUE, r: ORANGE}, idx=False)
    pointer(ax, l, y, "L", BLUE, below=False, length=0.45)
    pointer(ax, r, y, "R", ORANGE, below=False, length=0.45)
    ax.text(3.5, y - 0.35, msg, ha="center", va="top", fontsize=14, color=TEAL if k == 2 else "#222222")
ax.set_xlim(-0.5, 7.5); ax.set_ylim(-7.5, 2.7)
ax.set_title("Sorted two-sum, target 14: each step discards one end", fontsize=15)
save(fig, "dsa3_two_ends.png")
