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

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110); ax.set_xlim(0,10); ax.set_ylim(0,5.4); ax.axis("off")
box(ax,3.6,4.5,2.8,0.7,"Read the symptom",P)
qs=[("Wrong number?",0.1,"Context:\nslicer, filter,\ninteraction,\nrelationship",B),("Wrong person sees it?",2.6,"RLS:\nrole, Viewer,\nsecurity table",R),("Stale or failed?",5.1,"Refresh:\nschedule, gateway,\ncredentials",T),("Slow or messy?",7.6,"Performance /\ndesign:\nbiggest visual",O)]
for q,x,a,c in qs:
    box(ax,x,2.8,2.3,0.9,q,c,fs=9); arrow(ax,5,4.48,x+1.15,3.72,"#666",1.4)
    arrow(ax,x+1.15,2.78,x+1.15,2.0,c); ax.text(x+1.15,1.9,a,ha="center",va="top",fontsize=8.8,color=c)
ax.text(5,0.15,"Then: reproduce on the 8-row sample, change one thing, re-check against a hand number.",ha="center",fontsize=9.5)
ax.set_title("Which family of problem is this?",fontsize=12)
fig.tight_layout(); fig.savefig("ch11d_decision.png")
