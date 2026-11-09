import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
def box(ax,x,y,w,h,txt,col,fs=9.5,fc=None,tc="white"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc or col,ec=col,lw=1.5))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs,color=tc,fontweight="bold")
def arrow(ax,x1,y1,x2,y2,col="#444",lw=1.8):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=16,color=col,lw=lw))

import pandas as pd
d=pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006,1007,1008],"city":["Pune","Mumbai","Pune","Delhi","Mumbai","Mumbai","Delhi","Pune"],
 "amt":[998,1299,597,799,450,1298,2499,1400]})
d["fixed"]=d.amt/d.groupby("city").amt.transform("sum"); d["total"]=d.amt/d.amt.sum()
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110); x=np.arange(8); w_=.38
ax.bar(x-w_/2,d.fixed,w_,color=B,label="share of city total (FIXED city)")
ax.bar(x+w_/2,d.total,w_,color=O,label="share of grand total (EXCLUDE city)")
ax.set_xticks(x); ax.set_xticklabels([f"{i}\n{c}" for i,c in zip(d.id,d.city)],fontsize=8)
ax.set_ylabel("share",fontsize=11); ax.legend(frameon=False,fontsize=9.5)
ax.set_title("Same order, two levels of detail, two answers",fontsize=12)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch11d_lod.png")
