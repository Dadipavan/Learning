import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B,O,T,R="#2b4fd6","#b84a22","#357a70","#aa2d26"
fig,ax=plt.subplots(figsize=(8,4.2)); ax.set_xlim(0,16); ax.set_ylim(0,9); ax.axis("off")
def box(x,y,w,labels,fc,hi=None):
    n=len(labels); cw=w/n
    for i,l in enumerate(labels):
        c=O if hi==i else fc
        ax.add_patch(FancyBboxPatch((x+i*cw,y),cw,1,boxstyle="square,pad=0",fc="white",ec=c,lw=2.4 if hi==i else 1.4))
        ax.text(x+i*cw+cw/2,y+.5,l,ha="center",va="center",fontsize=10,color=c,fontweight="bold" if hi==i else None)
def arrow(x1,y1,x2,y2,c=B,lw=1.2):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",color=c,lw=lw))
box(5.5,7.4,5,["30","60"],B,None)
ax.text(5.3,7.9,"root",ha="right",fontsize=10,color=B)
mids=[(1.5,["10","20"]),(6.5,["40","50"]),(11.5,["70","80"])]
for x,l in mids: box(x,4.4,3,l,B,0 if x==6.5 and False else None)
box(6.5,4.4,3,["40","50"],B,0)
ax.text(.8,4.9,"branch",ha="right",fontsize=10,color=B)
arrow(6.5,7.4,3,5.4); arrow(8,7.4,8,5.4,O,2.2); arrow(9.5,7.4,13,5.4)
leaves=[(0,["5","8","10"]),(4.5,["31","35","40"]),(8.5,["41","44","50"]),(12.5,["71","75","80"])]
for x,l in leaves: box(x,1.4,3.2,l,T,None)
box(8.5,1.4,3.2,["41","44","50"],T,1)
ax.text(-.2,1.9,"leaf",ha="right",fontsize=10,color=T)
for (x,_),tx in zip(mids,[1.6,5.2,10.8]): pass
arrow(2.5,4.4,1.6,2.4); arrow(3.5,4.4,6,2.4); arrow(7.2,4.4,6,2.4); arrow(8.2,4.4,10,2.4,O,2.2); arrow(9.2,4.4,10.2,2.4); arrow(12,4.4,14,2.4)
ax.text(10.1,0.6,"found: key 44 and its row pointer",ha="center",fontsize=10,color=O)
ax.text(8,8.9,"Looking up key 44: 3 page reads, not a scan of every row",ha="center",fontsize=11.5,color="#222")
for x in (3.2,7.7,11.7): ax.plot([x,x+1.3],[1.9,1.9],alpha=0)
ax.annotate("",xy=(4.5,1.9),xytext=(3.2,1.9),arrowprops=dict(arrowstyle="<->",color="#888",ls=":"))
ax.annotate("",xy=(8.5,1.9),xytext=(7.7,1.9),arrowprops=dict(arrowstyle="<->",color="#888",ls=":"))
ax.annotate("",xy=(12.5,1.9),xytext=(11.7,1.9),arrowprops=dict(arrowstyle="<->",color="#888",ls=":"))
plt.tight_layout(); plt.savefig("ch10_btree.png",dpi=110)
