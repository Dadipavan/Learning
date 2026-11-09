from ch03_common import *
a = [3, 1, 4, 1, 5, 9, 2, 6]
P = [0]
for v in a:
    P.append(P[-1] + v)
fig, ax = new_fig()
draw_array(ax, a, y=2.2, x0=0.5, fills={i: BLUE for i in range(2, 6)}, idx=True)
ax.text(-0.2, 2.7, "a", ha="right", va="center", fontsize=16)
draw_array(ax, P, y=0, x0=0, fills={6: ORANGE, 2: RED}, idx=True)
ax.text(-0.2, 0.5, "P", ha="right", va="center", fontsize=16)
ax.text(4.5, -1.5, "sum of a[2..5] = P[6] - P[2] = 23 - 4 = 19", ha="center", fontsize=15, color=BLUE)
ax.text(4.5, -2.2, "P[i] = sum of the first i numbers", ha="center", fontsize=13, color="#555555")
ax.set_xlim(-1.2, 9.5); ax.set_ylim(-2.8, 3.8)
ax.set_title("Prefix sums: any range sum is one subtraction", fontsize=15)
save(fig, "dsa3_prefix.png")
