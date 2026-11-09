import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
fig, ax = canvas(9.5, 4.6)
box(ax, 1, 30, 14, 10, "raw\nfiles", GREY)
box(ax, 22, 30, 17, 10, "contract and\nschema check", BLUE)
box(ax, 46, 30, 17, 10, "row checks\n(null, unique,\nrange)", BLUE)
box(ax, 70, 30, 12, 10, "silver", TEAL)
box(ax, 86, 30, 12, 10, "volume and\nfresh. gate", PURPLE, fs=9)
box(ax, 46, 6, 17, 10, "quarantine\ntable + reason", ORANGE)
box(ax, 70, 6, 28, 10, "STOP and page a human\nif bad rate is above threshold", RED, fs=9)
for a, b in [(15, 22), (39, 46), (63, 70), (82, 86)]:
    arrow(ax, a + 0.3, 35, b - 0.3, 35)
arrow(ax, 54.5, 30, 54.5, 16.5, ORANGE, "bad rows", rad=0)
arrow(ax, 63.3, 11, 69.7, 11, RED, "rate?")
arrow(ax, 30.5, 30, 50, 16.5, ORANGE, "schema break", rad=0.0)
ax.text(1, 46, "Checks as gates: good rows continue, bad rows are kept with a reason, a large failure stops the run", fontsize=10.5, color=BLUE, weight="bold")
fig.savefig("de_check_pipeline.png", dpi=110, bbox_inches="tight")
