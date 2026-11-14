import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13})

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.axis("off");ax.set_xlim(0,16);ax.set_ylim(-0.6,5.6)
nodes=[]
def build(n,x,y,w,par=None):
    nodes.append((n,x,y,par))
    me=len(nodes)-1
    if n>=2:
        build(n-1,x-w,y-1,w/2,me); build(n-2,x+w,y-1,w/2,me)
build(5,8,5,4)
seen={}
for n,x,y,p in nodes:
    seen[n]=seen.get(n,0)+1
for n,x,y,p in nodes:
    if p is not None:
        ax.plot([nodes[p][1],x],[nodes[p][2],y],color="#888",lw=1.2,zorder=1)
for n,x,y,p in nodes:
    c=O if n==3 and seen[3]>1 else (R if n==2 else B)
    if n in(0,1): c=T
    ax.add_patch(Circle((x,y),0.33,fc=c,ec="black",zorder=2))
    ax.text(x,y,str(n),ha="center",va="center",color="white",fontsize=12,weight="bold",zorder=3)
ax.text(0.2,5.3,"fib(n) calls: fib(5) makes 15 calls",fontsize=13,weight="bold")
ax.text(10.0,0.2,"orange = fib(3) twice\nred = fib(2) three times\nteal = base cases",fontsize=12,color="black")
fig.tight_layout();fig.savefig("dsa6_fibtree.png")
