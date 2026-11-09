import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":14,"axes.labelsize":13})
from matplotlib.patches import Circle,Rectangle
h=[1,3,2,7,4,5,6]
fig,ax=plt.subplots(figsize=(8,4.6));ax.set_xlim(0,8);ax.set_ylim(-1.6,4.4);ax.axis("off")
pos={0:(4,3.7),1:(2,2.5),2:(6,2.5),3:(1,1.3),4:(3,1.3),5:(5,1.3),6:(7,1.3)}
for i in range(1,7):
    p=(i-1)//2
    ax.plot([pos[p][0],pos[i][0]],[pos[p][1],pos[i][1]],color="#555",lw=2,zorder=1)
for i,v in enumerate(h):
    c=[B,O,O,T,T,T,T][i]
    ax.add_patch(Circle(pos[i],0.38,fc=c,ec="none",zorder=2))
    ax.text(*pos[i],str(v),color="white",ha="center",va="center",fontsize=16,fontweight="bold",zorder=3)
    ax.text(pos[i][0]+0.5,pos[i][1]+0.3,"i=%d"%i,fontsize=11,color="#333")
for i,v in enumerate(h):
    ax.add_patch(Rectangle((0.6+i*0.9,-0.6),0.9,0.8,fc="white",ec="#333",lw=1.8))
    ax.text(1.05+i*0.9,-0.2,str(v),ha="center",va="center",fontsize=15)
    ax.text(1.05+i*0.9,-0.9,str(i),ha="center",va="center",fontsize=11,color="#555")
ax.text(4,0.55,"the same heap stored as a plain list",ha="center",fontsize=12)
ax.text(4,-1.4,"parent of i = (i-1)//2    children of i = 2i+1 and 2i+2",ha="center",fontsize=12,color=P)
ax.set_title("Min-heap: every parent is smaller than its children")
fig.tight_layout();fig.savefig("dsa1_heap.png",dpi=110)
