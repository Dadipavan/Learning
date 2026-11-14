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

X=np.array([[0,0],[0,1],[1,0],[1,1]]); y=np.array([0,1,1,0])
H=((X@np.array([[1,1],[1,1]])+np.array([-.5,-1.5]))>0).astype(float)
fig,axs=plt.subplots(1,2,figsize=(8,4.2))
for ax,P,t in [(axs[0],X.astype(float),"Before: input space (x1, x2)\nno straight line works"),(axs[1],H,"After: hidden space (h1=OR, h2=AND)\none line separates")]:
    for pt,l,src in zip(P,y,X):
        ax.scatter(*pt,s=170,marker="o" if l else "s",c=BL if l else RE,edgecolor="k",zorder=3)
        if not (ax is axs[1] and tuple(src)==(1,0)): ax.annotate(f"from ({src[0]},{src[1]})" if not (ax is axs[1] and tuple(src)==(0,1)) else "from (0,1) and (1,0)",pt,xytext=(6,8),textcoords="offset points",fontsize=8)
    ax.set_xlim(-.4,1.6); ax.set_ylim(-.4,1.6); ax.set_title(t,fontsize=9.5); ax.set_aspect("equal")
axs[0].set_xlabel("x1"); axs[0].set_ylabel("x2"); axs[1].set_xlabel("h1"); axs[1].set_ylabel("h2")
h=np.linspace(-.4,1.6,10); axs[1].plot(h,h-.5,color=TE,lw=2,ls="--"); axs[1].text(0.5,1.4,"h1 - h2 - 0.5 = 0",color=TE,fontsize=9)
axs[0].plot([-.4,1.6],[1.1,-.9],color=OR,ls=":",lw=2); axs[0].text(-.35,-.3,"any line cuts a diagonal",color=OR,fontsize=8.5)
fig.tight_layout(); fig.savefig("ch01d_xor_remap.png",dpi=110)
