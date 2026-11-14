from ch12_common import *
fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 5.4))
for a in (a1, a2): a.axis("off")
a1.set_xlim(-0.5, 9); a1.set_ylim(-1.6, 2.7)
vals = [1, 3, 4, 6, 8, 11]
cols = [None, None, "#cfe0f7", "#fbe0d2", None, None]
cells(a1, vals, 0.5, 0, colors=cols)
arrow(a1, 3.0, 1.9, 1.0, "L", B)
arrow(a1, 4.0, 1.9, 1.0, "R", O)
a1.text(0.5, -0.9, "sorted, target 10: 4 + 6 = 10 found, L and R moved inward from the ends", fontsize=13)
a1.set_title("Two pointers: walk inward, never go back", fontsize=15)
a2.set_xlim(-0.5, 9.5); a2.set_ylim(-1.6, 2.7)
s = "abcabcbb"
colors = [None, "#d4ece7", "#d4ece7", "#d4ece7", None, None, None, None]
cells(a2, list(s), 0.5, 0, colors=colors)
a2.add_patch(Rectangle((1.5, -0.08), 3, 1.06, fc="none", ec=T, lw=4))
arrow(a2, 2.0, 1.9, 1.0, "left", B)
arrow(a2, 4.0, 1.9, 1.0, "right", O)
a2.text(0.5, -0.9, "window 'bca' has no repeats; grow right, shrink left on a repeat", fontsize=13)
a2.set_title("Sliding window: a frame that grows and shrinks", fontsize=15)
plt.tight_layout(); plt.savefig("dsa12_pointers.png", dpi=110)
