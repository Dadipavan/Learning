import sys; sys.path.insert(0,"../../../tools/figs_dl")
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ch04_common import *
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
X,y=moons(); lrs=np.logspace(-4,1,30)
m=MLP([2,16,16,2],seed=0); m.forward(X); gW,gb=m.backward(y)
fig,ax=plt.subplots(figsize=(8,4.2))
ax.axhspan(1e-3,1e-2,color=T,alpha=.18,label="healthy band 1e-3 to 1e-2 (rule of thumb)")
for k,(c,n) in enumerate(zip([B,O,P],["layer 1","layer 2","layer 3"])):
    r=lrs*np.linalg.norm(gW[k])/np.linalg.norm(m.W[k]); ax.loglog(lrs,r,color=c,lw=2.5,label=n)
ax.axhline(1,color=R,ls="--",lw=1.5); ax.text(1.2e-4,1.25,"update as large as the weights",color=R,fontsize=9)
ax.set_xlabel("learning rate",fontsize=12); ax.set_ylabel("|update| / |weights|",fontsize=12)
ax.set_title("Update ratio at the first step grows linearly with the learning rate",fontsize=12)
ax.grid(alpha=.3,which="both"); ax.legend(fontsize=9,loc="lower right"); ax.tick_params(labelsize=10)
fig.tight_layout(); fig.savefig("ch04d_updateratio.png",dpi=110)
