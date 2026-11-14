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
box(ax,3.6,4.2,2.8,0.6,"What is the question?",B)
qs=[("Which data\ntrained model X?","lineage lookup\n(run record, hash)",0.1,O),("Get an old\ntraining set back","pointer + checkout,\nor AS OF query,\nthen verify hash",2.1,T),("Why did metrics\nchange?","change one pin\nat a time, then\ndiff the data",4.1,R),("What must\nrerun?","dependency graph:\nchanged inputs only",6.1,P),("Can we still\nreproduce it?","retention vs age,\nsnapshot when\ntraining",8.1,B)]
for q,a,x,c in qs:
    box(ax,x,2.6,1.8,0.95,q,c,fs=8); box(ax,x,0.7,1.8,1.1,a,c,fs=8); arrow(ax,(x+0.9,2.6),(x+0.9,1.8),c); arrow(ax,(5.0,4.2),(x+0.9,3.55),"#888")
ax.text(5,0.25,"Always finish with the check: recompute the hash and compare to the recorded one.",ha="center",fontsize=9,color=R)
ax.set_title("Decision flow for data and model versioning problems",fontsize=10)
fig.tight_layout(); fig.savefig("ch04d_decision.png",dpi=110)
