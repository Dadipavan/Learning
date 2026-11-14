import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
def score(lr,d): return np.exp(-((np.log10(lr)+2.3)**2)/0.5)-0.02*(d-0.3)**2
gx,gy=np.meshgrid(np.linspace(-4,-1,200),np.linspace(0,0.6,100))
Z=score(10**gx,gy)
fig,axs=plt.subplots(1,2,figsize=(9,4.2),sharey=True)
rng=np.random.default_rng(0)
lrs=np.linspace(-4,-1,3); ds=np.linspace(0,0.6,3)
for ax,title in zip(axs,["Grid: 9 trials, 3 learning rates","Random: 9 trials, 9 learning rates"]):
    ax.contourf(gx,gy,Z,levels=12,cmap="Blues",alpha=.8); ax.set_title(title,fontsize=11); ax.set_xlabel("log10(learning rate)")
G=[(a,b) for a in lrs for b in ds]; axs[0].scatter(*zip(*G),color="#b84a22",s=45,edgecolor="white")
R=(rng.uniform(-4,-1,9),rng.uniform(0,0.6,9)); axs[1].scatter(*R,color="#b84a22",s=45,edgecolor="white")
axs[0].set_ylabel("dropout")
fig.tight_layout(); fig.savefig("ch03_grid_vs_random.png",dpi=110)
