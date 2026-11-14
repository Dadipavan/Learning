import sys; sys.path.insert(0,"../../../tools/figs_dl")
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, warnings; warnings.simplefilter("ignore")
from ch04_common import *
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
def fit(sizes,ntr,noise,lr,steps,seed=0):
    Xa,ya=moons(ntr//2,noise,seed); Xv,yv=moons(300,noise,seed+7)
    m=MLP(sizes,seed=0); tr=[];va=[]
    for t in range(steps):
        m.forward(Xa); gW,gb=m.backward(ya)
        for k in range(len(m.W)): m.W[k]-=lr*gW[k]; m.b[k]-=lr*gb[k]
        tr.append(m.loss(Xa,ya)); va.append(m.loss(Xv,yv))
    return np.array(tr),np.array(va)
cases=[("A. Healthy",[2,16,2],200,.2,.3,300),("B. Overfitting",[2,128,128,2],24,.35,.03,800),
       ("C. Underfitting (linear model)",[2,2],200,.1,.5,300),("D. Learning rate too high",[2,16,2],200,.1,12.,300)]
fig,axs=plt.subplots(2,2,figsize=(8,4.2),sharex=False)
for ax,(n,sz,ntr,nz,lr,st) in zip(axs.ravel(),cases):
    tr,va=fit(sz,ntr,nz,lr,st)
    ax.plot(np.minimum(tr,3),color=B,lw=2,label="train"); ax.plot(np.minimum(va,3),color=O,lw=2,label="validation")
    ax.set_title(n,fontsize=10); ax.grid(alpha=.3); ax.tick_params(labelsize=8); ax.set_ylim(0,3 if n.startswith('D') else 1.3)
    ax.text(0.97,0.55,'final train %.2f\nfinal val %.2f'%(tr[-1],va[-1]),transform=ax.transAxes,ha='right',fontsize=8.5)
    print(n,[round(float(v),3) for v in (tr[0],tr[-1],va[-1],va.min())],int(va.argmin()))
axs[0,0].legend(fontsize=8); fig.supxlabel("training step",fontsize=10); fig.supylabel("loss (clipped at 3)",fontsize=10)
fig.tight_layout(); fig.savefig("ch04d_curves.png",dpi=110)
