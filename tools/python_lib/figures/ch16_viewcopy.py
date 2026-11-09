import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":15})

fig,axs=plt.subplots(1,2,figsize=(8,4.2),dpi=110)
for ax in axs:
    ax.set_xlim(-0.3,8.3);ax.set_ylim(-0.3,4.2);ax.axis("off")
def row(ax,y,vals,cols,x0=0.2):
    for i,v in enumerate(vals):
        ax.add_patch(Rectangle((x0+i,y),1,1,fc="white",ec=cols[i],lw=2.5))
        ax.text(x0+i+.5,y+.5,str(v),ha="center",va="center",fontsize=15)
ax=axs[0]
row(ax,2.8,[0,1,2,3,4,5,6,7],[B]*8,0)
row(ax,0.6,[2,3,4],[R]*3,2)
for i in range(3): ax.annotate("",xy=(2.5+i,1.6),xytext=(2.5+i,2.8),arrowprops=dict(arrowstyle="->",color=R,lw=2))
ax.set_title("Slice a[2:5] = VIEW\nsame memory",color=R,fontsize=13)
ax.text(4,0.1,"write through b -> a changes",ha="center",fontsize=11)
ax=axs[1]
row(ax,2.8,[0,1,2,3,4,5,6,7],[B]*8,0)
row(ax,0.6,[2,3,4],[T]*3,2)
ax.text(1.4,1.1,"new\nbuffer",ha="center",color=T,fontsize=11)
ax.set_title("a[[2,3,4]] = COPY\nown memory",color=T,fontsize=13)
ax.text(4,0.1,"write to b -> a unchanged",ha="center",fontsize=11)
plt.savefig("lib16_viewcopy.png",bbox_inches="tight")
