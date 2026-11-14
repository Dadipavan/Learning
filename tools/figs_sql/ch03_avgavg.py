import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R,V="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
c=[1,2,4,5,6]; spent=[4560,3600,3300,760,440]; n=[4,3,2,2,1]
aov=[s/k for s,k in zip(spent,n)]
fig,ax=plt.subplots(figsize=(8,4.2))
ax.bar([f"cust {x}\n({k} order{'s' if k>1 else ''})" for x,k in zip(c,n)],aov,color=B)
for i,a in enumerate(aov): ax.text(i,a+25,f"{a:.0f}",ha="center",fontsize=10)
ax.axhline(sum(aov)/5,color=R,ls="--"); ax.text(4.45,sum(aov)/5-95,"average of averages 962",color=R,ha="right",fontsize=9.5)
ax.axhline(sum(spent)/sum(n),color=T,lw=2); ax.text(4.45,sum(spent)/sum(n)+25,"true AOV 1055 (12660 / 12)",color=T,ha="right",fontsize=9.5)
ax.set_ylabel("average paid order value"); ax.set_title("Each customer's average counts once, but customers differ in order count",fontsize=10)
ax.set_ylim(0,1900)
for s in("top","right"): ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("ch03d_avgavg.png",dpi=110)
