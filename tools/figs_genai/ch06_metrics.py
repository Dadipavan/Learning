import matplotlib
matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
r=np.arange(1,11)
fig,(a,b)=plt.subplots(1,2,figsize=(8,4.2))
a.plot(r,1/r,marker="o",color="#aa2d26",lw=2,label="reciprocal rank 1/r")
a.plot(r,1/np.log2(r+1),marker="s",color="#2b4fd6",lw=2,label="nDCG weight 1/log2(r+1)")
a.plot(r,(r<=5).astype(float),marker="^",ls="none",ms=8,color="#357a70",label="hit@5 (all or nothing)")
a.set_xlabel("rank of the relevant chunk"); a.set_ylabel("credit"); a.set_title("How much credit each rank earns",fontsize=10)
a.legend(frameon=False,fontsize=8); a.spines[["top","right"]].set_visible(False)
q=["q1","q2","q3","q4","q5"]; rec=[1,1,0,1,1]; rr=[1,.5,0,.5,1]; nd=[.85,.631,0,.68,1]
x=np.arange(5)
b.bar(x-0.27,rec,0.27,color="#357a70",label="recall@5"); b.bar(x,rr,0.27,color="#aa2d26",label="RR"); b.bar(x+0.27,nd,0.27,color="#2b4fd6",label="nDCG@5")
b.set_xticks(x); b.set_xticklabels(q); b.set_title("Same 5 queries, three verdicts",fontsize=10)
b.legend(frameon=False,fontsize=8,loc="upper center",bbox_to_anchor=(0.5,-0.08),ncol=3); b.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch06d_metrics.png",dpi=110)
