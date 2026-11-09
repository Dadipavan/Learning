from ch12_common import *
pos = {1: (4, 3), 2: (2, 1.8), 3: (6, 1.8), 4: (1, 0.6), 5: (3, 0.6), 6: (5, 0.6), 7: (7, 0.6)}
E = [(1,2),(1,3),(2,4),(2,5),(3,6),(3,7)]
pre = {1:1,2:2,4:3,5:4,3:5,6:6,7:7}
post = {4:1,5:2,2:3,6:4,7:5,3:6,1:7}
fig, ax = plt.subplots(figsize=(8, 4.4)); ax.axis("off"); ax.set_xlim(-0.2, 8.4); ax.set_ylim(-1.0, 3.8)
for a, b in E: line(ax, pos[a], pos[b])
for k, p in pos.items():
    node(ax, p, "n%d" % k, fc="white", ec=B, r=0.38, fs=13)
    ax.text(p[0] - 0.62, p[1] + 0.3, str(pre[k]), color=T, fontsize=15, fontweight="bold", ha="center")
    ax.text(p[0] + 0.62, p[1] + 0.3, str(post[k]), color=O, fontsize=15, fontweight="bold", ha="center")
ax.text(0.2, -0.3, "green = order a node is first reached (preorder)", color=T, fontsize=13)
ax.text(0.2, -0.75, "orange = order it is finished (postorder)", color=O, fontsize=13)
ax.set_title("Tree DFS: visit on the way down, finish on the way up", fontsize=15)
plt.tight_layout(); plt.savefig("dsa12_tree.png", dpi=110)
