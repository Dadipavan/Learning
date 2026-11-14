import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rng=np.random.default_rng(0)
dims=[2,5,10,50,100,500,1000,5000]
ratio=[];cosstd=[]
for d in dims:
    X=rng.random((300,d)); q=rng.random(d)
    dist=np.linalg.norm(X-q,axis=1); ratio.append((dist.max()-dist.min())/dist.min())
    Z=rng.standard_normal((300,d)); Z/=np.linalg.norm(Z,axis=1,keepdims=True)
    c=(Z@Z.T)[np.triu_indices(300,1)]; cosstd.append(c.std())
fig,axs=plt.subplots(1,2,figsize=(8,4.2))
axs[0].loglog(dims,ratio,"o-",color="#2b4fd6",lw=2); axs[0].set_xlabel("dimension n"); axs[0].set_ylabel("(max − min) / min distance")
axs[0].set_title("Distances concentrate"); axs[0].grid(alpha=.25)
axs[1].loglog(dims,cosstd,"o-",color="#b84a22",lw=2,label="measured")
axs[1].loglog(dims,1/np.sqrt(dims),"--",color="#357a70",lw=2,label="1/√n")
axs[1].set_xlabel("dimension n"); axs[1].set_ylabel("std of cosine of random pairs"); axs[1].set_title("Random vectors become orthogonal"); axs[1].legend(); axs[1].grid(alpha=.25)
fig.tight_layout(); fig.savefig("ch05_high_dim.png",dpi=110)
