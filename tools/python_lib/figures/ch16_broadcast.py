import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":15})

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.set_xlim(0,17);ax.set_ylim(0,6);ax.axis("off")
def grid(x0,y0,vals,col,fc="white",alpha=1):
    for r,row in enumerate(vals):
        for c,v in enumerate(row):
            ax.add_patch(Rectangle((x0+c*1.0,y0-r*1.0),1,1,fc=fc,ec=col,lw=2,alpha=alpha))
            ax.text(x0+c*1.0+.5,y0-r*1.0+.5,str(v),ha="center",va="center",fontsize=14)
A=[[0,0,0],[10,10,10],[20,20,20]]
grid(0.2,3.3,[[0,0,0],[10,10,10],[20,20,20]],B)
ax.text(1.7,4.6,"A  shape (3, 3)",ha="center",color=B,fontweight="bold")
ax.text(3.7,2.8,"+",fontsize=26,ha="center")
grid(4.4,3.3,[[0,1,2]],O)
ax.text(5.9,4.6,"b  shape (3,)",ha="center",color=O,fontweight="bold")
for r in (1,2):
    grid(4.4,3.3-r,[[0,1,2]],O,fc="#fbe9e2",alpha=0.6)
ax.text(5.9,0.2,"b is stretched down\n(no copy is made)",ha="center",fontsize=11.5,color=O)
ax.text(8.2,2.8,"=",fontsize=26,ha="center")
grid(9.0,3.3,[[0,1,2],[10,11,12],[20,21,22]],T)
ax.text(10.5,4.6,"result  (3, 3)",ha="center",color=T,fontweight="bold")
ax.text(13.6,4.3,"Rules, right to left:",fontsize=12.5,fontweight="bold")
ax.text(13.6,3.5,"1. Pad shorter shape\n    with 1s on the left\n2. Sizes must match\n    or one must be 1\n3. Size 1 is stretched",fontsize=12,va="top")
plt.savefig("lib16_broadcast.png",bbox_inches="tight")
