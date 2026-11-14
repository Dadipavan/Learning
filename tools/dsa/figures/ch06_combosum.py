import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13})

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.axis("off");ax.set_xlim(-0.5,16.5);ax.set_ylim(-0.3,5.2)
# candidates [2,3,5], target 5 (sorted). nodes: (path, remaining)
def box(x,y,t,c="#eef",tc="black"):
    ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc,bbox=dict(boxstyle="round",fc=c,ec="black"))
def edge(x1,y1,x2,y2,l,c=B):
    ax.plot([x1,x2],[y1-0.25,y2+0.25],color="#888");ax.text((x1+x2)/2+0.3,(y1+y2)/2,l,fontsize=10.5,color=c)
box(8,4.7,"[]  left 5")
box(3,3.3,"[2]  left 3");edge(8,4.7,3,3.3,"2")
box(8,3.3,"[3]  left 2");edge(8,4.7,8,3.3,"3")
box(13,3.3,"[5]  left 0",T,"white");edge(8,4.7,13,3.3,"5")
box(1,1.8,"[2,2]  left 1");edge(3,3.3,1,1.8,"2")
box(5,1.8,"[2,3]  left 0",T,"white");edge(3,3.3,5,1.8,"3")
box(9,1.8,"[3,3] left -1",R,"white");edge(8,3.3,9,1.8,"3")
box(1,0.4,"[2,2,2] left -1",R,"white");edge(1,1.8,1,0.4,"2")
ax.text(13.2,2.0,"green = answer\nred = overshoot,\nprune (stop)",fontsize=12,ha="center",color="black")
ax.text(0,5.0,"candidates 2,3,5 ; target 5",fontsize=12,weight="bold",ha="left")
fig.tight_layout();fig.savefig("dsa6_combosum.png")
