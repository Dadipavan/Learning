import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch02common import *
fig, ax = newfig(); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
ax.text(5, 5.7, 'How Excel evaluates  =IF(OR(G4="Returned", H4>2000), "Review", "OK")  for row 4',
        ha="center", fontsize=10, fontweight="bold")
ax.text(0.1, 5.1, "Inputs from the row", fontsize=9, color="#555")
box(ax, 0.3, 4.1, 2.1, 0.7, 'G4 = "Returned"', TEAL)
box(ax, 0.3, 3.0, 2.1, 0.7, "H4 = 597", TEAL)
ax.text(3.2, 5.1, "Step 1: each test", fontsize=9, color="#555")
box(ax, 3.0, 4.1, 2.4, 0.7, 'G4="Returned"  ->  TRUE', BLUE)
box(ax, 3.0, 3.0, 2.4, 0.7, "H4>2000  ->  FALSE", BLUE)
arrow(ax, 2.4, 4.45, 3.0, 4.45); arrow(ax, 2.4, 3.35, 3.0, 3.35)
ax.text(6.2, 5.1, "Step 2: OR", fontsize=9, color="#555")
box(ax, 6.0, 3.55, 1.8, 0.8, "OR(TRUE, FALSE)\n-> TRUE", ORANGE)
arrow(ax, 5.4, 4.45, 6.0, 4.1); arrow(ax, 5.4, 3.35, 6.0, 3.8)
ax.text(8.2, 5.1, "Step 3: IF", fontsize=9, color="#555")
box(ax, 8.1, 3.55, 1.7, 0.8, 'IF(TRUE, ...)\n-> "Review"', PURPLE, bold=True)
arrow(ax, 7.8, 3.95, 8.1, 3.95)
ax.text(5, 2.2, "Excel works from the innermost parts outward. The inner results are\n"
        "TRUE or FALSE values, and each outer function receives those values, not the formulas.",
        ha="center", fontsize=10)
ax.text(5, 1.0, "Debug tip: Formulas > Evaluate Formula shows exactly these steps, one click at a time.",
        ha="center", fontsize=10, color=RED)
fig.tight_layout(); fig.savefig("ch02d_eval_flow.png")
