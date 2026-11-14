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

fig,ax=plt.subplots(figsize=(8,4.2)); ax.set_xlim(0,10); ax.set_ylim(0,5); ax.axis("off")
ins=[("code\ngit commit a1b2c3d",B,3.9),("data\nmd5 9e2f9675",O,2.7),("config\nC=1.0 seed=42",T,1.5),("environment\nlock file hash 4d2c9d",P,0.3)]
for t,c,y in ins:
    box(ax,0.2,y,2.6,0.85,t,c); arrow(ax,(2.8,y+0.42),(4.2,2.45),c)
box(ax,4.2,1.95,1.9,1.0,"training run\nrun id 19667813",R,fc="#fbeeed")
arrow(ax,(6.1,2.45),(7.2,2.45),R)
box(ax,7.2,1.95,2.4,1.0,"model artifact\nchurn v2\n(sha256 of file)",B)
arrow(ax,(8.4,1.95),(8.4,0.9),"#444","registry alias",(0.9,0))
box(ax,7.2,0.1,2.4,0.8,"serving: champion",T)
ax.text(4.2,4.4,"Lineage = these arrows, stored.\nChange any input and the run id changes.",fontsize=9,color="#222")
ax.set_title("Model lineage: four pinned inputs produce one traceable model",fontsize=10)
fig.tight_layout(); fig.savefig("ch04d_lineage.png",dpi=110)
