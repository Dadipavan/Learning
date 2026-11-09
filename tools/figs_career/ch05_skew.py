from common import *
import numpy as np
rng=np.random.default_rng(7); t=rng.lognormal(1.0,0.8,1000)
mean,med,p95=t.mean(),np.median(t),np.percentile(t,95)
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.hist(t,bins=50,color=BLUE,alpha=0.85)
for v,l,c in ((med,"median",TEAL),(mean,"mean",ORANGE),(p95,"95th percentile",RED)):
    ax.axvline(v,color=c,lw=2); ax.text(v+0.2,ax.get_ylim()[1]*0.9 if l!="mean" else ax.get_ylim()[1]*0.75,f"{l} {v:.1f}",color=c,fontsize=9)
ax.set_xlabel("response time (minutes)"); ax.set_ylabel("tickets"); clean(ax)
ax.set_title("Skewed data: the average hides the slow tail that customers feel",fontsize=10,fontweight="bold",loc="left")
fig.tight_layout(); fig.savefig("ch05d_skew.png")
