import sys; sys.path.insert(0,"../../../tools/figs_dl")
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, warnings; warnings.simplefilter("ignore")
from ch04_common import *
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
X,y=moons()
def run(clip=None,steps=300,lr=0.3):
    m=MLP([2,16,2],seed=0); r=np.random.default_rng(0); losses=[]; norms=[]
    for t in range(steps):
        idx=r.integers(0,len(X),32); xb=X[idx].copy(); yb=y[idx]
        if t in (100,200): xb=xb*30; yb=1-yb
        m.forward(xb); gW,gb=m.backward(yb); n=gnorm(gW,gb); norms.append(n)
        if clip and n>clip: f=clip/n; gW=[g*f for g in gW]; gb=[g*f for g in gb]
        for k in range(2): m.W[k]-=lr*gW[k]; m.b[k]-=lr*gb[k]
        losses.append(m.loss(X,y))
    return np.array(losses),np.array(norms)
l0,n0=run(); l1,n1=run(1.0)
fig,(a,b)=plt.subplots(1,2,figsize=(8,4.2))
a.plot(np.minimum(l0,3),color=O,lw=2,label="no clipping"); a.plot(l1,color=B,lw=2,label="clip at 1.0")
a.set_title("Loss on the full data",fontsize=11); a.set_xlabel("step",fontsize=10); a.set_ylabel("loss (clipped at 3)",fontsize=10); a.legend(fontsize=9); a.grid(alpha=.3)
b.semilogy(n0,color=O,lw=1.2,label="gradient norm (no clip)"); b.axhline(1.0,color=B,ls="--",lw=2,label="clip limit 1.0")
b.set_title("Gradient norm: two bad batches",fontsize=11); b.set_xlabel("step",fontsize=10); b.grid(alpha=.3,which="both"); b.legend(fontsize=9)
fig.tight_layout(); fig.savefig("ch04d_spike.png",dpi=110)
