import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13})

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.axis("off");ax.set_xlim(-0.3,16.3);ax.set_ylim(-0.2,4.9)
items=[1,2,3]
def rec(i,cur,x,y,w,px=None,py=None,lab=""):
    if px is not None:
        ax.plot([px,x],[py-0.2,y+0.2],color="#888",lw=1.3)
        ax.text((px+x)/2+(-0.35 if lab.startswith("skip") else 0.35),(py+y)/2,lab,fontsize=10.5,color=(R if lab.startswith("skip") else T),ha="center")
    if i==3:
        ax.text(x,y,"{"+",".join(map(str,cur))+"}",ha="center",va="center",fontsize=12,weight="bold",color="white",bbox=dict(boxstyle="round",fc=B,ec="black"))
        return
    ax.text(x,y,"i=%d  {%s}"%(i,",".join(map(str,cur))),ha="center",va="center",fontsize=11,bbox=dict(boxstyle="round",fc="#eef",ec="black"))
    rec(i+1,cur,x-w,y-1.5,w/2,x,y,"skip %d"%items[i])
    rec(i+1,cur+[items[i]],x+w,y-1.5,w/2,x,y,"take %d"%items[i])
rec(0,[],8,4.4,4)
fig.tight_layout();fig.savefig("dsa6_subsets.png")
