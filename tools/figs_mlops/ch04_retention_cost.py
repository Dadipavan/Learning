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
days=np.arange(0,91); table=100; price=0.023
fig,ax=plt.subplots(figsize=(8,4.2))
ax.plot(days,(table+table*1.0*days)*price,color=R,lw=2.2,label="edits spread across all files (every file rewritten daily)")
ax.plot(days,(table+table*0.02*days)*price,color=T,lw=2.2,label="edits clustered in one partition (2% rewritten daily)")
for d in (7,30,90): ax.axvline(d,color="#bbb",ls=":")
ax.set_xlabel("retention window (days of old versions kept)"); ax.set_ylabel("storage bill, USD per month (illustrative)")
ax.legend(fontsize=8,loc="upper left"); ax.set_title("A 100 GB table: retention is cheap or costly depending on how edits are laid out",fontsize=9.5)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch04d_retention_cost.png",dpi=110)
