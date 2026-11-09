from ch12_common import *
import numpy as np
a, b = "horse", "ros"
d = np.zeros((len(a)+1, len(b)+1), int)
d[:, 0] = range(len(a)+1); d[0, :] = range(len(b)+1)
for i in range(1, len(a)+1):
    for j in range(1, len(b)+1):
        d[i, j] = min(d[i-1, j]+1, d[i, j-1]+1, d[i-1, j-1] + (a[i-1] != b[j-1]))
fig, ax = plt.subplots(figsize=(8, 4.6)); ax.axis("off"); ax.set_xlim(-1.6, 4.6); ax.set_ylim(-6.9, 0.9); ax.set_aspect("equal")
for i in range(len(a)+1):
    for j in range(len(b)+1):
        v = d[i, j]
        fc = "#d4ece7" if (i, j) == (5, 3) else "white"
        ax.add_patch(Rectangle((j, -i-1), 1, 1, fc=fc, ec="#333", lw=1.8))
        ax.text(j+.5, -i-.5, str(v), ha="center", va="center", fontsize=18, fontweight="bold", color=R if (i, j) == (5, 3) else "black")
for j, ch in enumerate(" " + b): ax.text(j+.5, .3, "'%s'" % ch if ch != " " else "''", ha="center", fontsize=15, color=B, fontweight="bold")
for i, ch in enumerate(" " + a): ax.text(-.5, -i-.5, "'%s'" % ch if ch != " " else "''", ha="center", va="center", fontsize=15, color=O, fontweight="bold")
ax.text(4.2, -2.5, "cell (i, j) =\nfewest edits to turn\nfirst i letters of horse\ninto first j of ros", fontsize=12, va="center", color="#333")
ax.set_title("Edit distance table: answer 3 in the corner", fontsize=15)
plt.tight_layout(); plt.savefig("dsa12_editdp.png", dpi=110)
