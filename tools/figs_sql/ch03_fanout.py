import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
B,O,T,R,V="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
c=[1,2,3,4,5,6]; rows=[7,4,1,2,4,2]; orders=[4,3,1,2,3,1]
x=np.arange(6); fig,ax=plt.subplots(figsize=(8,4.2))
ax.bar(x-.2,rows,.4,color=O,label="COUNT(*) after joining order_items (wrong for 'orders')")
ax.bar(x+.2,orders,.4,color=T,label="COUNT(DISTINCT order_id) (right)")
for i in range(6):
    ax.text(i-.2,rows[i]+.12,rows[i],ha="center",fontsize=9); ax.text(i+.2,orders[i]+.12,orders[i],ha="center",fontsize=9)
ax.set_xticks(x); ax.set_xticklabels([f"cust {k}" for k in c]); ax.set_ylim(0,9.5)
ax.set_ylabel("count"); ax.legend(fontsize=8,loc="upper right",frameon=False)
ax.set_title("Fan-out: one order becomes one row per item line",fontsize=10.5)
for s in("top","right"): ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("ch03d_fanout.png",dpi=110)
