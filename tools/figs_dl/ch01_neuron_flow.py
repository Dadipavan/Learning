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

x=np.array([2.,3.,1.]); w=np.array([0.5,-0.4,1.2]); b=-0.3
p=x*w; z=p.sum()+b; a=1/(1+np.exp(-z))
fig,ax=plt.subplots(figsize=(8,4.2)); ax.set_xlim(0,100); ax.set_ylim(0,50); ax.axis("off")
names=["items","distance km","rush (0/1)"]
for i in range(3):
    y=36-i*14
    box(ax,1,y,13,6,f"x{i+1}={x[i]:g}\n{names[i]}",BL,8.5)
    arrow(ax,16,y+3,28,y+3)
    ax.text(22,y+5,f"w{i+1}={w[i]:g}",ha="center",fontsize=8.5,color=OR)
    box(ax,29,y,13,6,f"{x[i]:g} x {w[i]:g}\n= {p[i]:g}",TE,8.5)
    arrow(ax,44,y+3,56,22)
box(ax,57,17,15,10,f"sum {p.sum():g}\n+ bias {b:g}\nz = {z:.2f}",OR,9)
arrow(ax,74,22,80,22)
box(ax,81,17,16,10,f"sigmoid(z)\n= {a:.4f}",PU,9)
ax.text(50,4,"one neuron: multiply, add, add bias, bend (activation)",ha="center",fontsize=10)
ax.text(64.5,30,"weighted sum",ha="center",fontsize=8.5)
ax.text(89,30,"activation",ha="center",fontsize=8.5)
fig.tight_layout(); fig.savefig("ch01d_neuron_flow.png",dpi=110)
