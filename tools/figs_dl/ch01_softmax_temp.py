import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
BL,OR,TE,RE,PU,CR="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0","#f1e6c8"
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
def box(ax,x,y,w,h,t,c,fs=9.5,tc=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.25",fc=c,ec="#222",lw=1.2))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,color=tc or ("black" if c==CR else "white"))
def arrow(ax,x1,y1,x2,y2,col="#222"): ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",lw=1.6,color=col))

s=np.array([2.0,1.0,0.1]); fig,ax=plt.subplots(figsize=(8,4.2))
Ts=[0.25,1,2,5]; w=0.2
for i,(T,c) in enumerate(zip(Ts,[RE,BL,TE,PU])):
    e=np.exp((s-s.max())/T); p=e/e.sum()
    bars=ax.bar(np.arange(3)+(i-1.5)*w,p,w,color=c,label=f"T={T:g}")
    for xx,v in zip(np.arange(3)+(i-1.5)*w,p): ax.text(xx,v+.01,f"{v:.2f}",ha="center",fontsize=7.5)
ax.set_xticks(range(3)); ax.set_xticklabels(["score 2.0","score 1.0","score 0.1"]); ax.set_ylabel("probability"); ax.legend()
ax.set_title("softmax(scores / T): low T sharpens, high T flattens",fontsize=10)
fig.tight_layout(); fig.savefig("ch01d_softmax_temp.png",dpi=110)
