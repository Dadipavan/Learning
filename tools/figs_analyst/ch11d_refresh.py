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
rows=[("Bad: start 06:00",6.0,25,R),("Good: start 06:15",6.25,25,T),("Slow 45 min, 06:15",6.25,45,O),("Incremental, 10 min",6.25,10,B)]
for i,(n,s,dur,c) in enumerate(rows):
    y=len(rows)-i; ax.barh(y,dur/60,left=s,color=c,height=.5); ax.text(s+dur/60+0.03,y,f"ends {int(s)}:{int(round((s-int(s))*60+dur)):02d}" if (s-int(s))*60+dur<60 else f"ends 7:{int(round((s-int(s))*60+dur-60)):02d}",va="center",fontsize=9)
ax.axvline(6.0,color="#555",ls=":"); ax.text(6.0,4.75,"file lands 06:00",ha="center",fontsize=9)
ax.axvline(7.0,color=R,ls="--"); ax.text(7.0,4.75,"deadline 07:00",ha="center",fontsize=9,color=R)
ax.set_yticks(range(1,5)); ax.set_yticklabels([r[0] for r in rows][::-1],fontsize=9)
ax.set_xlim(5.9,7.3); ax.set_ylim(0.4,5.1)
ax.set_xticks([6,6.25,6.5,6.75,7]); ax.set_xticklabels(["06:00","06:15","06:30","06:45","07:00"])
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.set_title("Refresh timing against data arrival and deadline",fontsize=12)
fig.tight_layout(); fig.savefig("ch11d_refresh.png")
