import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch02common import *
fig, ax = newfig(); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
box(ax, 3.0, 5.2, 4.0, 0.65, "What does the answer look like?", PURPLE, fs=9.5, bold=True)
opts = [("One number\nfrom many rows", "SUMIFS, COUNTIFS,\nAVERAGEIFS,\nSUMPRODUCT", BLUE),
        ("A value fetched\nfrom another table", "XLOOKUP,\nINDEX+MATCH\n(bands: mode -1)", TEAL),
        ("A label or\nflag per row", "IF, IFS, SWITCH\nwith AND, OR", ORANGE),
        ("Messy text or\ndates", "TRIM, MID, FIND,\nDATE, EDATE,\nTEXT", RED),
        ("A list or table\nof rows", "FILTER, UNIQUE,\nSORTBY, TAKE,\nLET", PURPLE)]
xs = [0.1, 2.1, 4.1, 6.1, 8.0]
for x, (q, a, c) in zip(xs, opts):
    box(ax, x, 3.3, 1.85, 1.0, q, c, fs=8.5)
    box(ax, x, 1.5, 1.85, 1.1, a, c, fs=8)
    arrow(ax, x+0.92, 3.3, x+0.92, 2.62, c)
    arrow(ax, 5.0, 5.2, x+0.92, 4.32, "#777")
ax.text(5, 0.9, "Then always: 1) predict the answer by hand on 3 rows  2) check one total another way\n"
        "3) test an empty, a duplicate and a text-number case", ha="center", fontsize=9.5)
ax.text(5, 0.2, "If the result is wrong: COUNT rows, Evaluate Formula, trace precedents", ha="center", fontsize=9.5, color=RED)
fig.tight_layout(); fig.savefig("ch02d_playbook_flow.png")
