import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
fig, ax = canvas(10, 4.6)
ax.text(1, 48, "CI/CD for a data pipeline: every merge is tested before it can reach production", fontsize=10.5, color=BLUE, weight="bold")
steps = [("Pull request", BLUE), ("Lint +\nunit tests", BLUE), ("dbt build on\nCI schema\n(modified+)", TEAL), ("Review +\nmerge", BLUE), ("Deploy to\nstaging", ORANGE), ("Smoke test\n+ data checks", ORANGE), ("Promote to\nproduction", PURPLE)]
x = 1
for i, (txt, c) in enumerate(steps):
    box(ax, x, 26, 11.5, 11, txt, c, fs=8.3)
    if i: arrow(ax, x - 2.3, 31.5, x - 0.1, 31.5, GREY)
    x += 14.2
box(ax, 14, 6, 70, 9, "Failure at any gate stops the line and tells the author.\nProduction never sees code that did not pass the earlier steps.", RED, fs=9)
for xx in (7, 21, 36, 50, 64, 78, 92):
    pass
arrow(ax, 35, 25.6, 45, 15.4, RED, ls="--")
arrow(ax, 64, 25.6, 56, 15.4, RED, ls="--")
fig.savefig("de_cicd_flow.png", dpi=110, bbox_inches="tight")
