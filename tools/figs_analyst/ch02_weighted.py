import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch02common import *
fig, (a, b) = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110, gridspec_kw={"width_ratios": [1.5, 1]})
q = [r[4] for r in ROWS]; p = [r[5] for r in ROWS]
a.scatter(q, p, s=[x*60 for x in q], color=BLUE, alpha=0.7, edgecolor="white")
for r in ROWS: a.text(r[4]+0.12, r[5]+60, str(r[0]), fontsize=8)
a.axhline(798, color=ORANGE, ls="--"); a.text(3.6, 860, "simple AVERAGE = 798", color=ORANGE, fontsize=9)
a.axhline(491.58, color=TEAL, ls="--"); a.text(2.9, 540, "weighted = 491.58", color=TEAL, fontsize=9)
a.set_xlabel("Qty sold in the order (bubble size = Qty)", fontsize=10); a.set_ylabel("Price per unit (Rs)", fontsize=10)
a.set_title("Big orders sit at low prices", fontsize=11)
b.bar(["AVERAGE\n(each row 1)", "SUMPRODUCT\n/ SUM(Qty)"], [798, 491.58], color=[ORANGE, TEAL])
for i, v in enumerate([798, 491.58]): b.text(i, v+15, "%.2f" % v, ha="center", fontsize=10)
b.set_title("Same data, two answers", fontsize=11); b.set_ylim(0, 950)
for ax in (a, b): clean(ax)
fig.tight_layout(); fig.savefig("ch02d_weighted.png")
