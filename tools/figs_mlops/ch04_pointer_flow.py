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

fig,ax=plt.subplots(figsize=(8,4.2)); ax.set_xlim(0,10); ax.set_ylim(0,5.2); ax.axis("off")
box(ax,0.2,3.3,2.4,1.2,"working folder\ndata/train.csv\n(20 GB, git-ignored)",B)
box(ax,0.2,0.6,2.4,1.2,"train.csv.dvc\n(pointer: md5, size)",O)
box(ax,4.0,3.3,2.4,1.2,"local cache\n.dvc/cache/9e/2f96...\n(object named by hash)",T)
box(ax,4.0,0.6,2.4,1.2,"git history\ncommit A: pointer d844\ncommit B: pointer 9e2f",O)
box(ax,7.5,3.3,2.3,1.2,"remote storage\nS3 / GCS / Azure\n(shared by team)",P)
arrow(ax,(2.6,4.1),(4.0,4.1),B,"dvc add")
arrow(ax,(1.4,3.3),(1.4,1.8),O,"writes",(0.45,0))
arrow(ax,(2.6,1.2),(4.0,1.2),O,"git commit")
arrow(ax,(6.4,4.1),(7.5,4.1),P,"dvc push")
arrow(ax,(7.5,3.6),(6.4,3.6),P,"dvc pull",(0,-0.3))
arrow(ax,(5.2,1.8),(5.2,3.3),R,"git checkout old commit,\nthen dvc checkout",(1.15,0))
ax.set_title("Data versioning: git holds labels, storage holds contents, the hash joins them",fontsize=10)
fig.tight_layout(); fig.savefig("ch04d_pointer_flow.png",dpi=110)
