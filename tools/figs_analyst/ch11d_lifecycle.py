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
xs=[0.1,2.1,4.1,6.1,8.1]; names=["Source\n(files, SQL)","Model\n(star, DAX)","Report\n(Desktop)","Service\n(workspace)","Viewers\n(app, Teams)"]
cols=[T,B,B,P,O]
for x,n,c in zip(xs,names,cols): box(ax,x,3.0,1.8,1.2,n,c)
for i in range(4): arrow(ax,xs[i]+1.82,3.6,xs[i+1]-0.02,3.6)
notes=[(1.0,"clean, types,\nkeys"),(3.0,"relationships,\nmeasures, RLS roles"),(5.0,"layout, slicers,\ndrill, theme"),(7.0,"refresh, gateway,\nroles, pipeline"),(9.0,"Viewer role:\nRLS applies")]
for x,t in notes: ax.text(x,2.45,t,ha="center",va="top",fontsize=8.5,color="#333")
ax.add_patch(Rectangle((2.05,0.35),3.9,0.9,fc="#f3e1dd",ec=R,lw=1.2)); ax.text(4.0,0.8,"Design time: rules live in the model",ha="center",va="center",fontsize=9,color=R)
ax.add_patch(Rectangle((6.05,0.35),3.9,0.9,fc="#e3e8fb",ec=B,lw=1.2)); ax.text(8.0,0.8,"Run time: refresh and access checks",ha="center",va="center",fontsize=9,color=B)
ax.set_title("From data to a secure, shared report",fontsize=12)
fig.tight_layout(); fig.savefig("ch11d_lifecycle.png")
