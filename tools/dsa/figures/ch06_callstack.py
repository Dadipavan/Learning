import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13})

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.set_xlim(0,10);ax.set_ylim(0,6);ax.axis("off")
# going down: frames stacked, then returns
frames=["fact(1)  returns 1","fact(2)  waits: 2 * fact(1)","fact(3)  waits: 3 * fact(2)","fact(4)  waits: 4 * fact(3)"]
cols=[T,B,B,B]
for i,(f,c) in enumerate(zip(frames,cols)):
    ax.add_patch(FancyBboxPatch((0.4,0.4+i*1.1),5.2,0.9,boxstyle="round,pad=0.02",fc=c,ec="black",alpha=0.9))
    ax.text(3.0,0.85+i*1.1,f,ha="center",va="center",color="white",fontsize=13,weight="bold")
ax.text(3.0,5.15,"Call stack (top = newest call)",ha="center",fontsize=14,weight="bold")
ax.annotate("",xy=(6.3,4.5),xytext=(6.3,1.0),arrowprops=dict(arrowstyle="->",color=O,lw=3))
ax.text(6.55,2.7,"calls go\nup the stack",color=O,fontsize=13,va="center")
ax.text(9.9,4.3,"Then returns\nflow back down:",ha="right",fontsize=13,color=R,weight="bold")
ax.text(9.9,3.1,"fact(1) gives 1\nfact(2) gives 2\nfact(3) gives 6\nfact(4) gives 24",ha="right",fontsize=13,color=R,va="top")
fig.tight_layout();fig.savefig("dsa6_callstack.png")
