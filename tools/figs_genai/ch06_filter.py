import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
rng=np.random.default_rng(0)
N,d,k=20000,32,10
X=rng.normal(size=(N,d)).astype("float32"); X/=np.linalg.norm(X,axis=1,keepdims=True)
Q=rng.normal(size=(100,d)).astype("float32"); Q/=np.linalg.norm(Q,axis=1,keepdims=True)
S=Q@X.T; order=np.argsort(-S,axis=1)
sels=[0.5,0.3,0.2,0.1,0.05,0.02,0.01]
res={1:[],5:[],20:[]}
for sel in sels:
    allow=rng.random(N)<sel
    for mult in res:
        fetched=order[:,:k*mult]
        res[mult].append(np.mean([allow[f].sum() if allow[f].sum()<k else k for f in fetched]))
fig,ax=plt.subplots(figsize=(8,4.2))
ax.plot([s*100 for s in sels],[k]*len(sels),color="#357a70",lw=2.5,marker="s",label="pre-filter (filter inside the search)")
for mult,col in [(20,"#2b4fd6"),(5,"#b84a22"),(1,"#aa2d26")]:
    ax.plot([s*100 for s in sels],res[mult],color=col,lw=2,marker="o",label=f"post-filter, fetch {k*mult} then filter")
ax.set_xscale("log"); ax.set_xticks([1,2,5,10,20,50]); ax.set_xticklabels(["1%","2%","5%","10%","20%","50%"])
ax.set_xlabel("share of chunks the filter keeps (log scale)"); ax.set_ylabel("results returned (wanted 10)")
ax.set_title("Post-filtering silently returns fewer results as the filter gets narrower")
ax.legend(frameon=False,fontsize=8.5,loc="center left"); ax.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch06d_filter.png",dpi=110)
