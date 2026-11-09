import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":15})

fig,axs=plt.subplots(1,2,figsize=(8,4.2),dpi=110)
a=np.array([[1,2,3],[4,5,6]])
for ax,(ax_i,title,col) in zip(axs,[(0,"sum(axis=0): collapse rows\nresult [5 7 9]",B),(1,"sum(axis=1): collapse columns\nresult [6 15]",O)]):
    ax.set_xlim(-0.2,4.6);ax.set_ylim(-1.8,2.4);ax.axis("off")
    for r in range(2):
        for c in range(3):
            ax.add_patch(Rectangle((c,1-r),1,1,fc="white",ec="#444",lw=1.5))
            ax.text(c+.5,1.5-r,str(a[r,c]),ha="center",va="center",fontsize=18)
    if ax_i==0:
        for c in range(3):
            ax.annotate("",xy=(c+.5,-.75),xytext=(c+.5,-.05),arrowprops=dict(arrowstyle="->",color=col,lw=2.5))
            ax.text(c+.5,-1.35,str(a[:,c].sum()),ha="center",fontsize=18,color=col,fontweight="bold")
    else:
        for r in range(2):
            ax.annotate("",xy=(3.4,1.5-r),xytext=(2.95,1.5-r),arrowprops=dict(arrowstyle="->",color=col,lw=2.5))
            ax.text(3.9,1.5-r,str(a[r].sum()),ha="left",va="center",fontsize=18,color=col,fontweight="bold")
    ax.set_title(title,color=col,fontsize=13)
fig.tight_layout();plt.savefig("lib16_axis.png",bbox_inches="tight")
