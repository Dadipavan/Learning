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

fig,axs=plt.subplots(1,2,figsize=(8,4.2),dpi=110)
rng=np.random.default_rng(3)
ax=axs[0]; ax.set_xlim(0,1280); ax.set_ylim(720,0); ax.set_title("Before: crowded, misaligned",fontsize=11,color=R)
for i in range(11):
    x=rng.integers(0,950); y=rng.integers(0,560); w_=rng.integers(200,330); h=rng.integers(110,200)
    ax.add_patch(Rectangle((x,y),w_,h,fc=["#e3e8fb","#f3e1dd","#dcebe8"][i%3],ec="#555",alpha=.85,lw=1))
ax.text(640,700,"11 visuals, 6 slicers, no order",ha="center",fontsize=9)
ax=axs[1]; ax.set_xlim(0,1280); ax.set_ylim(720,0); ax.set_title("After: grid, 5 visuals",fontsize=11,color=T)
for x in (20,440,860): ax.add_patch(Rectangle((x,20),400,110,fc=B,ec=B)); ax.text(x+200,75,"card 400 px",color="white",ha="center",fontsize=9)
ax.add_patch(Rectangle((20,150),780,550,fc="#e3e8fb",ec=B)); ax.text(410,420,"trend (line)\n780 x 550",ha="center",fontsize=10)
ax.add_patch(Rectangle((820,150),440,550,fc="#dcebe8",ec=T)); ax.text(1040,420,"sorted bar\n440 x 550",ha="center",fontsize=10)
for a in axs: a.set_xticks([]); a.set_yticks([]); a.set_aspect("equal")
fig.tight_layout(); fig.savefig("ch11d_layout.png")
