import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch02common import *
fig, axs = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110)
cols = [(r"Without \$ (wrong)", ["=H2*J1", "=H3*J2", "=H4*J3"], ["J1 = 18%", "J2 = empty", "J3 = empty"], RED),
        (r"With \$J\$1 (right)", [r"=H2*\$J\$1", r"=H3*\$J\$1", r"=H4*\$J\$1"], ["J1 = 18%", "J1 = 18%", "J1 = 18%"], TEAL)]
for ax, (title, f, tgt, c) in zip(axs, cols):
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.set_title(title, fontsize=11, color=c, fontweight="bold")
    ax.text(1.5, 5.3, "cell", fontsize=9, color="#555", ha="center")
    ax.text(4.2, 5.3, "formula", fontsize=9, color="#555", ha="center")
    ax.text(8.0, 5.3, "points at", fontsize=9, color="#555", ha="center")
    for i in range(3):
        y = 4.1 - i*1.5
        box(ax, 0.5, y, 2.0, 0.8, "I%d" % (i+2), BLUE)
        box(ax, 3.0, y, 2.6, 0.8, f[i], c)
        box(ax, 6.4, y, 3.2, 0.8, tgt[i], c)
        arrow(ax, 2.5, y+0.4, 3.0, y+0.4); arrow(ax, 5.6, y+0.4, 6.4, y+0.4)
fig.suptitle("Fill down copies the formula one row at a time", fontsize=11)
fig.tight_layout(); fig.savefig("ch02d_copy_refs.png")
