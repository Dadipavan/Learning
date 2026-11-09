import sys; sys.path.insert(0,"../../../tools/figs_dl")
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, warnings; warnings.simplefilter("ignore")
from ch04_common import *
B,O,T,R,P="#2b4fd6","#b84a22","#357a70",  "#aa2d26","#6a2fd0"
X,y=moons(); m=MLP([2,16,2],seed=0); lrs=np.logspace(-4,2,120); L=[]
for lr in lrs:
    m.forward(X); gW,gb=m.backward(y); L.append(m.loss(X,y))
    for k in range(2): m.W[k]-=lr*gW[k]; m.b[k]-=lr*gb[k]
L=np.array(L); np.save("/tmp/c4/lrrange.npy",L)
fig,ax=plt.subplots(figsize=(8,4.2)); ax.semilogx(lrs,np.minimum(L,5),color=B,lw=2.5)
j=L.argmin()
ax.axvspan(lrs[j]/10,lrs[j]/3,color=T,alpha=.25,label="pick a rate in here (3x to 10x below the minimum)")
ax.axvline(lrs[j],color=O,ls="--",label="loss minimum at lr = %.2f, then it blows up"%lrs[j])
ax.set_ylim(0,5); ax.set_xlabel("learning rate (grows every step)",fontsize=12); ax.set_ylabel("loss (clipped at 5)",fontsize=12)
ax.set_title("Learning-rate range test: raise the rate each step and watch the loss",fontsize=12)
ax.grid(alpha=.3,which="both"); ax.legend(fontsize=10); fig.tight_layout(); fig.savefig("ch04d_lrrange.png",dpi=110)
print(lrs[j], L[j], lrs[j]/10, lrs[j]/3, lrs[np.argmax(L>1)])
