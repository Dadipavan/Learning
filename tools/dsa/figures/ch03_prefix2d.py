from ch03_common import *
g = [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7]]
R, C = 4, 5
P = [[0] * (C + 1) for _ in range(R + 1)]
for i in range(R):
    for j in range(C):
        P[i + 1][j + 1] = g[i][j] + P[i][j + 1] + P[i + 1][j] - P[i][j]
r1, c1, r2, c2 = 1, 1, 2, 3
total = P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]
fig, ax = plt.subplots(1, 2, figsize=(9, 3.8))
def grid(a, M, x0, fills, title):
    a.axis("off"); a.set_aspect("equal")
    for i, row in enumerate(M):
        for j, v in enumerate(row):
            a.add_patch(Rectangle((j, -i), 1, 1, fc=LIGHT.get(fills.get((i, j)), "white"), ec="#333333", lw=1.4))
            a.text(j + .5, -i + .5, str(v), ha="center", va="center", fontsize=14)
    a.set_xlim(-0.2, len(M[0]) + 0.2); a.set_ylim(-len(M) + 0.8, 1.8)
    a.set_title(title, fontsize=14)
f1 = {(i, j): BLUE for i in range(r1, r2 + 1) for j in range(c1, c2 + 1)}
grid(ax[0], g, 0, f1, "grid: blue block sums to %d" % total)
f2 = {(r2 + 1, c2 + 1): BLUE, (r1, c2 + 1): RED, (r2 + 1, c1): RED, (r1, c1): ORANGE}
grid(ax[1], P, 0, f2, "P: blue - red - red + orange")
fig.text(0.5, 0.02, "%d - %d - %d + %d = %d" % (P[r2+1][c2+1], P[r1][c2+1], P[r2+1][c1], P[r1][c1], total),
         ha="center", fontsize=15, color=BLUE)
save(fig, "dsa3_prefix2d.png")
