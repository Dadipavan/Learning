import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
rng=np.random.default_rng(0)
dims=[2,5,10,20,50,100,200,500,1000]; ratio=[]
for d in dims:
    X=rng.normal(size=(5000,d)); q=rng.normal(size=d); dist=np.linalg.norm(X-q,axis=1); ratio.append(dist.max()/dist.min())
fig,ax=plt.subplots(figsize=(8,4.2))
ax.plot(dims,ratio,marker="o",color="#2b4fd6",lw=2)
ax.set_xscale("log"); ax.set_yscale("log"); ax.axhline(1,color="#aa2d26",ls="--"); ax.text(2.2,1.05,"ratio 1 = everything equally far",color="#aa2d26",fontsize=8.5)
ax.set_xlabel("number of dimensions"); ax.set_ylabel("farthest distance / nearest distance")
ax.set_title("Random points: near and far stop looking different as dimensions grow")
ax.spines[["top","right"]].set_visible(False); fig.tight_layout(); fig.savefig("ch06d_concentration.png",dpi=110)
