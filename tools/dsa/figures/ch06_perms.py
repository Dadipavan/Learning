import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13})

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.axis("off");ax.set_xlim(-0.5,16.5);ax.set_ylim(-0.3,4.9)
ax.text(8,4.6,"[]",ha="center",va="center",fontsize=13,bbox=dict(boxstyle="round",fc="#eef",ec="black"))
firsts=[1,2,3];x0=[2.7,8,13.3]
for f,x in zip(firsts,x0):
    ax.plot([8,x],[4.4,3.5],color="#888")
    ax.text(x,3.3,"[%d]"%f,ha="center",va="center",fontsize=13,bbox=dict(boxstyle="round",fc="#eef",ec="black"))
    rest=[v for v in firsts if v!=f]
    for k,s in enumerate(rest):
        xx=x+(-1.3 if k==0 else 1.3)
        ax.plot([x,xx],[3.1,2.2],color="#888")
        ax.text(xx,2.0,"[%d,%d]"%(f,s),ha="center",va="center",fontsize=12,bbox=dict(boxstyle="round",fc="#eef",ec="black"))
        last=[v for v in rest if v!=s][0]
        ax.plot([xx,xx],[1.8,1.1],color="#888")
        ax.text(xx,0.7,"%d%d%d"%(f,s,last),ha="center",va="center",fontsize=12,weight="bold",color="white",bbox=dict(boxstyle="round",fc=T,ec="black"))
ax.text(0,4.5,"level 0: 3 choices\nlevel 1: 2 choices\nlevel 2: 1 choice",fontsize=11,color=O,va="top")
ax.text(16.5,0.0,"3 x 2 x 1 = 6 leaves",fontsize=12,color=R,ha="right",weight="bold")
fig.tight_layout();fig.savefig("dsa6_perms.png")
