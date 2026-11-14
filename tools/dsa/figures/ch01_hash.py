import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":14,"axes.labelsize":13})
from matplotlib.patches import Rectangle
fig,ax=plt.subplots(figsize=(8,4.4))
ax.set_xlim(0,10);ax.set_ylim(-0.7,8.4);ax.axis("off")
keys=[("'ann'",5,B),("'bob'",2,O),("'cy'",6,T),("'dee'",2,P)]
for i in range(8):
    y=7-i
    ax.add_patch(Rectangle((6,y-0.4),1.6,0.8,fc="white",ec="#333",lw=1.8))
    ax.text(5.6,y,str(i),ha="right",va="center",fontsize=13)
vals={5:"31",2:"27",6:"40"}
for i,v in vals.items():
    ax.text(6.8,7-i,v,ha="center",va="center",fontsize=14,color="#222")
ax.add_patch(Rectangle((7.9,7-2-0.4),1.6,0.8,fc="white",ec="#333",lw=1.8))
ax.text(8.7,5,"33",ha="center",va="center",fontsize=14)
ax.annotate("",xy=(7.9,5),xytext=(7.6,5),arrowprops=dict(arrowstyle="->",lw=2))
for k,(name,slot,c) in enumerate(keys):
    y=7-k*2.0
    ax.text(0.2,y,name,fontsize=15,color=c,va="center",fontweight="bold")
    ax.text(1.5,y,"hash %% 8 = %d"%slot,fontsize=12,color=c,va="center")
    ax.annotate("",xy=(6,7-slot),xytext=(3.4,y),arrowprops=dict(arrowstyle="->",color=c,lw=2.2))
ax.text(8.7,2.2,"'bob' and 'dee'\nshare slot 2:\na collision, handled\nby chaining",ha="center",fontsize=11.5,color=R)
ax.set_title("A dict: key, hash, slot (illustrative numbers)")
fig.tight_layout();fig.savefig("dsa1_hash.png",dpi=110)
