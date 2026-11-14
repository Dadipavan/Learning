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

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
labs=["Before","Fix matrix\nonly","Fix 5 small\nonly","Fix both"]
big=[9.5,1.5,9.5,1.5]; small=[2.0,2.0,0.5,0.5]
ax.bar(labs,big,color=O,label="matrix"); ax.bar(labs,small,bottom=big,color=B,label="5 small visuals")
for i,(a,b) in enumerate(zip(big,small)): ax.text(i,a+b+0.2,f"{a+b:.1f} s",ha="center",fontsize=10)
ax.set_ylabel("page time (seconds, visuals added)",fontsize=10); ax.legend(frameon=False,fontsize=10)
ax.set_title("Fix the biggest slice first",fontsize=12)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch11d_perf.png")
