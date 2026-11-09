import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
from sklearn.cluster import KMeans
def make(spread,N=30000,d=32,groups=60,seed=0):
    rng=np.random.default_rng(seed); centers=rng.normal(size=(groups,d))*spread
    X=centers[rng.integers(0,groups,N)]+rng.normal(size=(N,d)); X=(X/np.linalg.norm(X,axis=1,keepdims=True)).astype("float32")
    Q=X[rng.choice(N,200,replace=False)]+0.15*rng.normal(size=(200,d)).astype("float32")
    return X,(Q/np.linalg.norm(Q,axis=1,keepdims=True)).astype("float32")
fig,ax=plt.subplots(figsize=(8,4.2))
for name,spread,col in [("well separated groups",3.0,"#357a70"),("overlapping groups",0.8,"#b84a22")]:
    X,Q=make(spread); truth=np.argsort(-(Q@X.T),axis=1)[:,:10]
    km=KMeans(100,n_init=1,random_state=0).fit(X); C=km.cluster_centers_.astype("float32")
    lists=[np.nonzero(km.labels_==j)[0] for j in range(100)]
    xs=[];ys=[]
    for nprobe in [1,2,3,5,10,20,40,70]:
        hit=sc=0
        for qi,q in enumerate(Q):
            cand=np.concatenate([lists[j] for j in np.argsort(-(C@q))[:nprobe]]); sc+=len(cand)
            hit+=len(set(cand[np.argsort(-(X[cand]@q))[:10]].tolist())&set(truth[qi].tolist()))
        xs.append(100*sc/len(Q)/len(X)); ys.append(hit/2000)
    ax.plot(xs,ys,marker="o",color=col,lw=2,label=name)
    for x,y,n in zip(xs,ys,[1,2,3,5,10,20,40,70]):
        if n in ((2,) if spread>2 else (1,10,20)): ax.annotate(f"nprobe={n}",(x,y),textcoords="offset points",xytext=(8,-4) if spread>2 else (8,-14),fontsize=8,color=col)
ax.axhline(0.95,color="#aa2d26",ls="--",lw=1); ax.text(52,0.955,"95% recall target",color="#aa2d26",fontsize=8.5)
ax.set_xlabel("share of the data scanned per query (%)"); ax.set_ylabel("recall@10 vs exact search")
ax.set_title("IVF: harder data needs about 10 times more scanning for 95% recall")
ax.legend(frameon=False,loc="lower right"); ax.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch06d_ivf_curves.png",dpi=110)
