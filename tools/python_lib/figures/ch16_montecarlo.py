import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":15})

rng=np.random.default_rng(7)
fig,axs=plt.subplots(1,2,figsize=(8,4.2),dpi=110,gridspec_kw={"width_ratios":[1,1.2]})
p=rng.random((600,2));inside=(p**2).sum(1)<=1
ax=axs[0]
ax.scatter(*p[inside].T,s=8,color=B,label="inside");ax.scatter(*p[~inside].T,s=8,color=O,label="outside")
t=np.linspace(0,np.pi/2,100);ax.plot(np.cos(t),np.sin(t),"k",lw=2)
ax.set_aspect("equal");ax.set_title("600 random points");ax.legend(loc="upper right",fontsize=10)
n=np.arange(1,200001);est=4*np.cumsum((rng.random((200000,2))**2).sum(1)<=1)/n
ax=axs[1];ax.semilogx(n,est,color=B,lw=1.8);ax.axhline(np.pi,color=R,ls="--",lw=2,label="true pi")
ax.set_ylim(2.8,3.5);ax.set_xlabel("number of points");ax.set_ylabel("estimate of pi");ax.legend();ax.set_title("Estimate settles down")
fig.tight_layout();plt.savefig("lib16_montecarlo.png",bbox_inches="tight")
