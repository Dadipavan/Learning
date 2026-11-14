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

X=np.array([[0,0],[0,1],[1,0],[1,1]])
def train(y,epochs=10):
    w=np.zeros(2); b=0.0
    for ep in range(epochs):
        err=0
        for x,t in zip(X,y):
            p=1 if w@x+b>0 else 0; d=t-p
            if d: w=w+d*x; b+=d; err+=1
        if err==0: break
    return w,b
fig,axs=plt.subplots(1,3,figsize=(8,4.2),sharey=True)
for ax,(n,y) in zip(axs,[("AND",[0,0,0,1]),("OR",[0,1,1,1]),("XOR (fails)",[0,1,1,0])]):
    w,b=train(np.array(y))
    gx,gy=np.meshgrid(np.linspace(-.5,1.5,50),np.linspace(-.5,1.5,50))
    ax.contourf(gx,gy,(w[0]*gx+w[1]*gy+b>0).astype(int),levels=[-.5,.5,1.5],colors=["#f4d9d3","#d3dcf7"])
    for pt,t in zip(X,y):
        ax.scatter(*pt,s=120,marker="o" if t else "s",c=BL if t else RE,edgecolor="k",zorder=3)
    ax.set_title(f"{n}\nw=({w[0]:g},{w[1]:g}) b={b:g}",fontsize=9); ax.set_xlim(-.5,1.5); ax.set_ylim(-.5,1.5); ax.set_xlabel("x1")
    ax.set_aspect("equal")
axs[0].set_ylabel("x2")
fig.text(0.5,0.01,"blue circle = target 1, red square = target 0, blue shade = region the neuron calls 1",ha="center",fontsize=8.5)
fig.tight_layout(rect=(0,0.04,1,1)); fig.savefig("ch01d_boundaries.png",dpi=110)
