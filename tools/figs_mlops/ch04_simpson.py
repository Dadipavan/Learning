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

import numpy as np
fig,ax=plt.subplots(figsize=(8,4.2)); w=0.35
labels=["group A","group B","overall"]
v1=[0.90,0.62,0.844]; v2=[0.91,0.64,0.721]
ax.bar(np.arange(3),v1,w,color=B,label="model v1 (test mix 800 A / 200 B)")
ax.bar(np.arange(3)+w,v2,w,color=O,label="model v2 (test mix 300 A / 700 B)")
for i in range(3):
    ax.text(i,v1[i]+0.01,f"{v1[i]:.3f}",ha="center",fontsize=9); ax.text(i+w,v2[i]+0.01,f"{v2[i]:.3f}",ha="center",fontsize=9)
ax.set_xticks(np.arange(3)+w/2); ax.set_xticklabels(labels); ax.set_ylim(0.4,1.05); ax.set_ylabel("accuracy"); ax.legend(fontsize=8,loc="upper right")
ax.set_title("Both groups improved, yet overall fell: the test-set mix changed",fontsize=10)
for s in ("top","right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("ch04d_simpson.png",dpi=110)
