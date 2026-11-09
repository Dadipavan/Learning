from ch03_common import *
s = "abcdbea"
rows = [(0, 3, "r=3: window abcd, all different"),
        (2, 4, "r=4: b repeats, l jumps to 2 (after old b)"),
        (2, 6, "r=6: window cdbea, length 5 (best)")]
fig, ax = new_fig()
for k, (l, r, msg) in enumerate(rows):
    y = -k * 3.0
    draw_array(ax, list(s), y=y, fills={i: TEAL for i in range(l, r + 1)}, idx=False)
    ax.add_patch(Rectangle((l, y), r - l + 1, 1, fc="none", ec=TEAL, lw=4))
    pointer(ax, l, y, "l", BLUE, below=False, length=0.4)
    pointer(ax, r, y, "r", ORANGE, below=False, length=0.4)
    ax.text(3.5, y - 0.3, msg, ha="center", va="top", fontsize=14)
ax.set_xlim(-0.3, 7.3); ax.set_ylim(-6.8, 2.4)
ax.set_title("Variable window: grow r, move l only when a rule breaks", fontsize=15)
save(fig, "dsa3_var_window.png")
