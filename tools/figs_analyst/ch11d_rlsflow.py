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

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110); ax.set_xlim(0,10); ax.set_ylim(0,5.2); ax.axis("off")
box(ax,0.2,3.7,2.4,1.1,"Security table\nEmail | Region",P)
box(ax,3.8,3.7,2.4,1.1,"DimCity\n[Region] filter",B)
box(ax,7.4,3.7,2.4,1.1,"FactSales\nrows left",T)
arrow(ax,2.62,4.25,3.78,4.25); arrow(ax,6.22,4.25,7.38,4.25)
ax.text(3.2,4.6,"IN ...",fontsize=9,ha="center"); ax.text(6.8,4.6,"1 to *",fontsize=9,ha="center")
ax.text(1.4,3.45,"USERPRINCIPALNAME()\nmatches the login",ha="center",va="top",fontsize=8.5)
rows=[("asha","West","6 rows, 6,042",O),("ravi","North","2 rows, 3,298",B),("cfo","North+West","8 rows, 9,340",T),("new.joiner","(none)","0 rows, 0",R)]
for i,(u,r,t,c) in enumerate(rows):
    y=2.0-i*0.5
    ax.text(0.3,y,u,fontsize=10,fontweight="bold",color=c); ax.text(2.4,y,"role gives "+r,fontsize=10); ax.text(6.2,y,"-> "+t,fontsize=10,color=c)
ax.set_title("Dynamic RLS: one role, filter flows down the relationship",fontsize=12)
fig.tight_layout(); fig.savefig("ch11d_rlsflow.png")
