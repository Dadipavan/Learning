from ch12_common import *
g = ["11000", "11000", "00100", "00011"]
ids = {}
cols = [B, O, T]
lab = [[-1]*5 for _ in range(4)]
n = 0
def fill(r, c, k):
    if r<0 or c<0 or r>=4 or c>=5 or g[r][c]!="1" or lab[r][c]!=-1: return
    lab[r][c]=k
    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)): fill(r+dr,c+dc,k)
for r in range(4):
    for c in range(5):
        if g[r][c]=="1" and lab[r][c]==-1:
            fill(r,c,n); n+=1
fig, ax = plt.subplots(figsize=(8, 4.2)); ax.axis("off"); ax.set_xlim(-0.3, 5.3); ax.set_ylim(-0.3, 4.6); ax.set_aspect("equal")
for r in range(4):
    for c in range(5):
        k = lab[r][c]
        fc = cols[k] if k >= 0 else "#eef1f5"
        ax.add_patch(Rectangle((c, 3 - r), 1, 1, fc=fc, ec="white", lw=3))
        ax.text(c + .5, 3 - r + .5, "island %d" % (k + 1) if False else (str(k + 1) if k >= 0 else "~"), ha="center", va="center",
                fontsize=20, color="white" if k >= 0 else "#99a", fontweight="bold")
ax.set_title("Grid DFS: each unvisited land cell starts a new island (count = 3)", fontsize=14)
plt.tight_layout(); plt.savefig("dsa12_islands.png", dpi=110)
