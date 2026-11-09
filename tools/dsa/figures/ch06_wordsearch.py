import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13})

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.set_xlim(0,12);ax.set_ylim(0,4);ax.set_aspect("equal");ax.axis("off")
g=["CAT","DOE","BAR"]
path=[(0,0),(0,1),(0,2)]
g=["CAR","ATE","DOG"]
path=[(0,0),(1,0),(1,1)]   # C A T ? 
g=["CAR","ATE","DOG"]
word="CATE"
path=[(0,0),(1,0),(1,1),(1,2)]
for r in range(3):
    for c in range(3):
        on=(r,c) in path
        ax.add_patch(Rectangle((c,2-r+0.5),1,1,fc=("#cfe6df" if on else "#f2f2f2"),ec="black"))
        ax.text(c+0.5,2-r+1.0,g[r][c],ha="center",va="center",fontsize=22,weight="bold")
pts=[(c+0.5,2-r+1.0) for r,c in path]
for a,b in zip(pts,pts[1:]):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",color=O,lw=3,shrinkA=14,shrinkB=14))
ax.text(4.2,3.2,"Find the word CATE",fontsize=14,weight="bold")
ax.text(4.2,2.5,"1. start at C (row 0, col 0)",fontsize=12.5)
ax.text(4.2,2.0,"2. A is below: move down",fontsize=12.5)
ax.text(4.2,1.5,"3. T is on the right: move right",fontsize=12.5)
ax.text(4.2,1.0,"4. E is on the right: move right",fontsize=12.5)
ax.text(4.2,0.4,"Mark each used cell, unmark on the way back",fontsize=12.5,color=R,weight="bold")
fig.tight_layout();fig.savefig("dsa6_wordsearch.png")
