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

fig,ax=plt.subplots(figsize=(8,4.2))
files=[("f0",0,1,"v0 only"),("f1",1,3,"v1, v2 (live)"),("f2",2,3,"v2 (live)")]
cols=[R,B,T]
for i,(n,a,b,l) in enumerate(files):
    ax.barh(i,b-a,left=a,color=cols[i],height=0.5); ax.text(a+0.05,i,f"{n}: in {l}",va="center",color="white",fontsize=9)
ax.axvline(1.0,color="#444",ls=":"); ax.axvline(2.0,color="#444",ls=":")
ax.text(0.5,2.65,"commit v0\n05 Jan",ha="center",fontsize=8); ax.text(1.5,2.65,"commit v1\n20 Jan: rewrite f0 as f1",ha="center",fontsize=8); ax.text(2.5,2.65,"commit v2\n10 Feb: append f2",ha="center",fontsize=8)
ax.annotate("VACUUM deletes f0 here:\nversion 0 is gone for good",xy=(1.0,0),xytext=(1.1,-0.9),arrowprops=dict(arrowstyle="->",color=R),color=R,fontsize=9)
ax.set_ylim(-1.3,3.3); ax.set_xlim(0,3); ax.set_yticks([0,1,2]); ax.set_yticklabels(["f0","f1","f2"]); ax.set_xticks([0.5,1.5,2.5]); ax.set_xticklabels(["after v0","after v1","after v2"])
ax.set_title("Table log: which data files belong to which version",fontsize=10)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch04d_timetravel.png",dpi=110)
