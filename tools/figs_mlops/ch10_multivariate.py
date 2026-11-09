import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rng=np.random.default_rng(0)
ref=rng.multivariate_normal([0,0],[[1,.8],[.8,1]],1500); new=rng.multivariate_normal([0,0],[[1,-.8],[-.8,1]],1500)
fig,axs=plt.subplots(1,3,figsize=(10,3.6),gridspec_kw={"width_ratios":[1.4,1,1]})
axs[0].scatter(*ref.T,s=5,alpha=.35,color="#2b4fd6",label="reference"); axs[0].scatter(*new.T,s=5,alpha=.35,color="#b84a22",label="today")
axs[0].set_title("Joint view: clearly different",fontsize=10); axs[0].set_xlabel("feature 0"); axs[0].set_ylabel("feature 1"); axs[0].legend(markerscale=3,fontsize=8)
for j,ax in enumerate(axs[1:]):
    ax.hist(ref[:,j],bins=30,alpha=.5,color="#2b4fd6",density=True); ax.hist(new[:,j],bins=30,alpha=.5,color="#b84a22",density=True)
    ax.set_title(f"Feature {j} alone: identical",fontsize=10); ax.set_xlabel(f"feature {j}")
fig.tight_layout(); fig.savefig("ch10_multivariate.png",dpi=110)
