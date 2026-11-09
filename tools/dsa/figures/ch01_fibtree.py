import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":14,"axes.labelsize":13})
from matplotlib.patches import Circle
nodes=[]  # (label,x,y,parent,repeat)
seen=set()
leaf=[0]
def build(n,depth,parent):
    idx=len(nodes);rep=n in seen and n>1
    nodes.append([n,0,-depth,parent,rep]);seen.add(n)
    if n<=1: x=leaf[0];leaf[0]+=1;nodes[idx][1]=x;return idx
    a=build(n-1,depth+1,idx);b=build(n-2,depth+1,idx)
    nodes[idx][1]=(nodes[a][1]+nodes[b][1])/2;return idx
build(5,0,None)
fig,ax=plt.subplots(figsize=(8.6,4.8))
for lab,x,y,p,rep in nodes:
    if p is not None: ax.plot([x,nodes[p][1]],[y,nodes[p][2]],color="#777",lw=1.6,zorder=1)
for lab,x,y,p,rep in nodes:
    c=R if rep else B
    ax.add_patch(Circle((x,y),0.33,fc=c,ec="none",zorder=2))
    ax.text(x,y,"f(%d)"%lab,color="white",ha="center",va="center",fontsize=9.5,fontweight="bold",zorder=3)
ax.set_xlim(-0.8,leaf[0]-0.2);ax.set_ylim(-4.7,0.7);ax.set_aspect("equal");ax.axis("off")
ax.text(leaf[0]-0.5,-3.2,"blue: first time computed\nred: repeated work\n(a cache would answer these)",ha="right",va="top",fontsize=11.5,color="#222")
ax.set_title("Recursion tree of fib(5): 15 calls, only 6 different inputs")
fig.tight_layout();fig.savefig("dsa1_fibtree.png",dpi=110)
