import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch02common import *
fig, (a, b) = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110)
amts = [998, 1299, 597, 799, 450, 1298, 2499, 1400]
cols = [BLUE]*8; cols[2] = RED
a.bar(range(2, 10), amts, color=cols)
a.set_xticks(range(2, 10)); a.set_xticklabels(["H%d" % i for i in range(2, 10)], fontsize=8)
a.set_title("Column H: H4 is text \"597\"\n(Excel skips it)", fontsize=10)
a.set_ylabel("Amount", fontsize=10)
lab = ["expected\nSUM", "SUM\nshown", "COUNT\nshown", "rows"]
b.bar(["SUM\nexpected", "SUM\nshown"], [9340, 8743], color=[TEAL, RED])
for i, v in enumerate([9340, 8743]): b.text(i, v+120, "{:,}".format(v), ha="center", fontsize=10)
b.text(0.5, 10000, "gap = 597 = H4;  COUNT = 7 but 8 rows", ha="center", fontsize=9.5, color=RED)
b.set_ylim(0, 11000); b.set_yticks([0,2000,4000,6000,8000]); b.set_title("The gap equals one cell", fontsize=10)
for ax in (a, b): clean(ax)
fig.tight_layout(); fig.savefig("ch02d_text_number.png")
