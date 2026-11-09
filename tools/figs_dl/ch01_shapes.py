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

fig,ax=plt.subplots(figsize=(8,4.2)); ax.set_xlim(0,100); ax.set_ylim(0,50); ax.axis("off")
items=[(1,"X\n(32, 20)\n32 orders,\n20 features",BL),(22,"X @ W1 + b1\nW1 (20, 64)\nb1 (64,)\n= (32, 64)",TE),(43,"ReLU\nsame shape\n(32, 64)",OR),(62,"H @ W2 + b2\nW2 (64, 32)\n= (32, 32)\nthen ReLU",TE),(82,"H @ W3 + b3\nW3 (32, 1)\n= (32, 1)\nsigmoid -> p",PU)]
for x,t,c in items: box(ax,x,22,15,14,t,c,8.5)
for a,b in [(17,21),(38,42),(59,61.5),(79,81.5)]: arrow(ax,a,29,b,29)
ax.text(50,12,"Rule: (N, in) @ (in, out) = (N, out). The inner numbers must match; the batch size N never changes.",ha="center",fontsize=9)
ax.text(50,6,"Parameters: 20*64+64 = 1344,  64*32+32 = 2080,  32*1+1 = 33,  total 3457",ha="center",fontsize=9,color=OR)
fig.tight_layout(); fig.savefig("ch01d_shapes.png",dpi=110)
