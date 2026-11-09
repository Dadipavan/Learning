import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R,V="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
c=[1,2,4,5,6]; sp=[4560,3600,3300,760,440]
fig,ax=plt.subplots(figsize=(8,4.2))
cols=[T if s>1500 else "#bbbbbb" for s in sp]
ax.bar([f"cust {k}" for k in c],sp,color=cols)
for i,s in enumerate(sp): ax.text(i,s+80,str(s),ha="center",fontsize=10)
ax.axhline(1500,color=R,ls="--"); ax.text(4.45,1580,"HAVING threshold 1500",color=R,ha="right",fontsize=9.5)
ax.text(1,5300,"kept (green)  /  removed by HAVING (grey)",ha="center",fontsize=9.5,color="#333")
ax.set_ylim(0,5800); ax.set_ylabel("paid spend (WHERE already removed the 2 non-paid orders)",fontsize=8.5)
ax.set_title("HAVING keeps or drops whole groups, after the sums exist",fontsize=10.5)
for s in("top","right"): ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("ch03d_having.png",dpi=110)
