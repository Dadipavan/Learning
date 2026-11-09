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
 "day":[3,3,4,5,6,7,9,10],"amt":[998,1299,597,799,450,1298,2499,1400]})
fig,axs=plt.subplots(1,3,figsize=(8,4.2),dpi=110,gridspec_kw={"width_ratios":[1,1.5,1.5]})
c=d.groupby("city").amt.sum().reindex(["Delhi","Mumbai","Pune"])
axs[0].bar(c.index,c.values,color=[B,B,O]); axs[0].set_title("Click Pune",fontsize=10)
for i,v in enumerate(c.values): axs[0].text(i,v+40,f"{v:,}",ha="center",fontsize=8)
ad=d.groupby("day").amt.sum().reindex(range(3,11),fill_value=0)
pu=d[d.city=="Pune"].groupby("day").amt.sum().reindex(range(3,11),fill_value=0)
axs[1].bar(ad.index,ad.values,color="#c9c9c9"); axs[1].bar(pu.index,pu.values,color=O)
axs[1].set_title("Highlight: Pune inside all",fontsize=10)
axs[2].bar(pu.index,pu.values,color=O); axs[2].set_title("Filter: Pune only (2,995)",fontsize=10)
for a in axs: a.tick_params(labelsize=8); [a.spines[s].set_visible(False) for s in ("top","right")]
axs[1].set_xlabel("day of Jan 2025",fontsize=9); axs[2].set_xlabel("day of Jan 2025",fontsize=9)
fig.tight_layout(); fig.savefig("ch11d_crossfilter.png")
