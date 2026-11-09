from ch03_common import *
n = 6
diff = [0, 5, 0, 0, -5, 0]
res = [0, 5, 5, 5, 0, 0]
fig, ax = new_fig()
draw_array(ax, [0] * n, y=5.2, fills={}, idx=True)
ax.text(-0.3, 5.7, "start", ha="right", va="center", fontsize=14)
ax.text(6.4, 5.7, "goal: add 5 to indexes 1..3", va="center", fontsize=14, color=BLUE)
draw_array(ax, diff, y=2.6, fills={1: TEAL, 4: RED}, idx=False)
ax.text(-0.3, 3.1, "diff", ha="right", va="center", fontsize=14)
ax.text(6.4, 3.1, "d[1] += 5 and d[4] -= 5", va="center", fontsize=14, color=TEAL)
draw_array(ax, res, y=0, fills={i: BLUE for i in (1, 2, 3)}, idx=False)
ax.text(-0.3, 0.5, "running\nsum", ha="right", va="center", fontsize=14)
ax.text(6.4, 0.5, "running sum of diff\ngives the final array", va="center", fontsize=14, color=BLUE)
ax.set_xlim(-2.5, 12.5); ax.set_ylim(-0.5, 6.6)
ax.set_title("Difference array: two edits instead of a loop", fontsize=15)
save(fig, "dsa3_diff.png")
