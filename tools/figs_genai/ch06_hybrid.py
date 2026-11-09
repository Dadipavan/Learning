import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
# rank of the right chunk per query, from the hybrid experiment in section 6.7 (99 = not retrieved)
ranks={"paraphrase":{"BM25":[99,99,99,2],"dense":[1,1,1,1],"hybrid (RRF)":[1,1,1,2]},
       "exact code":{"BM25":[1,1,1],"dense":[2,1,1],"hybrid (RRF)":[1,1,1]},
       "mixed":{"BM25":[1,1,1],"dense":[2,2,1],"hybrid (RRF)":[1,1,1]}}
mrr=lambda r: np.mean([0 if x==99 else 1/x for x in r])
fig,ax=plt.subplots(figsize=(8,4.2)); x=np.arange(3)
for i,(m,c) in enumerate([("BM25","#b84a22"),("dense","#2b4fd6"),("hybrid (RRF)","#357a70")]):
    v=[mrr(ranks[g][m]) for g in ranks]
    ax.bar(x+(i-1)*0.26,v,0.26,color=c,label=m)
    for xi,vi in zip(x,v): ax.text(xi+(i-1)*0.26,vi+0.02,f"{vi:.2f}",ha="center",fontsize=8)
ax.set_xticks(x); ax.set_xticklabels([f"{g}\n({len(ranks[g]['BM25'])} queries)" for g in ranks]); ax.set_ylim(0,1.15)
ax.set_ylabel("mean reciprocal rank (higher is better)"); ax.set_title("Each retriever fails somewhere; the merge stays near the best one")
ax.legend(frameon=False,loc="upper center",bbox_to_anchor=(0.5,-0.2),ncol=3); ax.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch06d_hybrid.png",dpi=110)
