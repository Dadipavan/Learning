from common import *
fig, ax = canvas(8, 4.4)
ax.set_xlim(0, 10); ax.set_ylim(0, 5.6)
box(ax, 3.9, 4.4, 2.2, 0.8, "object", GREY)
box(ax, 3.9, 3.2, 2.2, 0.8, "A", BLUE, bold=True)
box(ax, 1.4, 1.9, 2.2, 0.8, "B(A)", ORANGE, bold=True)
box(ax, 6.4, 1.9, 2.2, 0.8, "C(A)", TEAL, bold=True)
box(ax, 3.9, 0.5, 2.2, 0.8, "D(B, C)", PURPLE, bold=True)
for a in [(5.0, 4.4, 5.0, 4.0), (4.5, 3.2, 2.9, 2.7), (5.5, 3.2, 7.1, 2.7), (2.9, 1.9, 4.4, 1.3), (7.1, 1.9, 5.6, 1.3)]:
    arrow(ax, a[2], a[3], a[0], a[1], GREY)
ax.text(0.1, 5.3, "Arrows point from child to parent", fontsize=10, color=GREY)
ax.text(0.1, 0.3, "D.__mro__ :  D, B, C, A, object\nA shows up once, after both B and C.", fontsize=10.5, color=PURPLE)
save(fig, "ch08_mro.png")
