import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13})

fig,axs=plt.subplots(1,2,figsize=(8,4.2),dpi=110)
def board(ax,queens,title,attacked=(),bad=None):
    ax.set_xlim(0,4);ax.set_ylim(0,4);ax.set_aspect("equal");ax.axis("off")
    for r in range(4):
        for c in range(4):
            col="#f2f2f2" if (r+c)%2==0 else "#c8d0e8"
            if (r,c) in attacked: col="#f3c6c0"
            ax.add_patch(Rectangle((c,3-r),1,1,fc=col,ec="black"))
    for r,c in queens:
        ax.text(c+0.5,3-r+0.5,"Q",ha="center",va="center",fontsize=24,weight="bold",color=(R if (r,c)==bad else B))
    ax.set_title(title,fontsize=13)
board(axs[0],[(0,1),(1,3),(2,0),(3,2)],"Solution: columns 1,3,0,2")
att=set()
for (r,c) in [(0,0),(1,2)]:
    for rr in range(4):
        for cc in range(4):
            if rr==r or cc==c or abs(rr-r)==abs(cc-c): att.add((rr,cc))
board(axs[1],[(0,0),(1,2)],"Dead end: Q at (0,0),(1,2)\nthird row is all pink (attacked)",attacked=att)
fig.tight_layout();fig.savefig("dsa6_nqueens.png")
