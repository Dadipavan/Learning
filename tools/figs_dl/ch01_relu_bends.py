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

f=lambda x:x**2
xs=np.linspace(-2,2,400)
fig,axs=plt.subplots(1,3,figsize=(8,4.2),sharey=True)
for ax,k in zip(axs,[2,4,8]):
    t=np.linspace(-2,2,k+1); s=np.diff(f(t))/np.diff(t); c=np.concatenate([[s[0]],np.diff(s)])
    yhat=f(-2)+sum(c[i]*np.maximum(0,xs-t[i]) for i in range(k))
    err=np.abs(yhat-f(xs)).max()
    ax.plot(xs,f(xs),color="#999",lw=3,label="target x^2"); ax.plot(xs,yhat,color=BL,lw=2,label="ReLU net")
    ax.scatter(t[:-1],f(t[:-1]),color=OR,zorder=3,s=25)
    ax.set_title(f"{k} hidden ReLU units\nmax error {err:.4f}",fontsize=9.5); ax.set_xlabel("x")
axs[0].legend(fontsize=8,loc="upper center"); axs[0].set_ylabel("output")
fig.text(0.5,0.01,"orange dots = where each ReLU unit bends the line (its hinge)",ha="center",fontsize=8.5)
fig.tight_layout(rect=(0,0.04,1,1)); fig.savefig("ch01d_relu_bends.png",dpi=110)
