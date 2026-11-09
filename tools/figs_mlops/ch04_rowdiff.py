import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
def box(ax,x,y,w,h,txt,c,fs=9,fc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc or "white",ec=c,lw=2))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,color="#222")
def arrow(ax,a,b,c="#444",txt=None,off=(0,0.12),fs=8):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="->",color=c,lw=1.8))
    if txt: ax.text((a[0]+b[0])/2+off[0],(a[1]+b[1])/2+off[1],txt,ha="center",fontsize=fs,color=c)

import numpy as np
v1=[(1,25,0),(2,40,1),(3,33,0),(4,51,1)]; v2=[(1,25,0),(2,41,1),(3,33,0),(5,29,0)]
fig,axs=plt.subplots(1,3,figsize=(8,4.2),gridspec_kw={"width_ratios":[1.2,1.2,1]})
def table(ax,rows,colors,title):
    ax.axis("off"); ax.set_title(title,fontsize=10)
    t=ax.table(cellText=[[str(x) for x in r] for r in rows],colLabels=["id","age","churn"],loc="center",cellLoc="center")
    t.scale(1,1.8)
    for i,c in enumerate(colors):
        for j in range(3): t[i+1,j].set_facecolor(c)
table(axs[0],v1,["white","#f6d9c9","white","#f0c4c0"],"version 1")
table(axs[1],v2,["white","#f6d9c9","white","#cfe8e2"],"version 2")
axs[2].bar(["v1","v2"],[0.5,0.25],color=[B,O]); axs[2].set_ylim(0,0.7); axs[2].set_title("positive rate",fontsize=10)
for i,v in enumerate([0.5,0.25]): axs[2].text(i,v+0.02,str(v),ha="center")
for s in ("top","right"): axs[2].spines[s].set_visible(False)
fig.text(0.5,0.05,"orange = value changed (id 2 age 40 to 41)   red = removed (id 4)   green = added (id 5)   Row count is 4 and 4, yet 3 rows moved.",ha="center",fontsize=8)
fig.tight_layout(rect=(0,0.08,1,1)); fig.savefig("ch04d_rowdiff.png",dpi=110)
