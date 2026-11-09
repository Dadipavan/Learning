import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":15})

x=np.linspace(0,1000,500)
fig,axs=plt.subplots(1,2,figsize=(8,4.2),dpi=110)
ax=axs[0]
z=np.linspace(0,120,400)
ax.semilogy(z,np.exp(z.astype(np.float32)).clip(max=3.4e38) if False else np.exp(z),color=B,lw=2.5)
ax.axhline(float(np.finfo(np.float32).max),color=R,ls="--",lw=2);ax.text(2,float(np.finfo(np.float32).max)*3,"float32 max",color=R,fontsize=11)
ax.set_xlabel("z");ax.set_ylabel("exp(z)");ax.set_title("exp grows explosively")
ax=axs[1]
s=np.array([2.0,1.0,0.1]);shift=np.linspace(-3,3,50)
def sm(v):
    e=np.exp(v-v.max());return e/e.sum()
labs=["class A","class B","class C"]
vals=np.array([sm(s+d) for d in shift])
for i,c in enumerate([B,O,T]): ax.plot(shift,vals[:,i],color=c,lw=3-i*.6,ls=["-","--",":"][i],label=labs[i])
ax.set_xlabel("constant added to all scores");ax.set_ylabel("probability");ax.set_title("Shift changes nothing");ax.legend(fontsize=10);ax.set_ylim(0,1)
fig.tight_layout();plt.savefig("lib16_softmax.png",bbox_inches="tight")
