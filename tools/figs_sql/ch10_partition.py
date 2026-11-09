import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B,O,T,G="#2b4fd6","#b84a22","#357a70","#999999"
fig,ax=plt.subplots(figsize=(8,4.2)); ax.set_xlim(0,16); ax.set_ylim(0,8); ax.axis("off")
ax.text(8,7.5,"Table orders PARTITION BY RANGE (order_date), one partition per month",ha="center",fontsize=11.5)
ax.text(8,6.4,"WHERE order_date >= '2024-03-01' AND order_date < '2024-04-01'",ha="center",fontsize=10,color=B,family="monospace")
months=["Jan","Feb","Mar","Apr","May","Jun"]
for i,m in enumerate(months):
    x=1+i*2.4; hit=(m=="Mar")
    ax.add_patch(FancyBboxPatch((x,2.2),2,2.4,boxstyle="round,pad=0.05",fc="#e8efff" if hit else "#f2f2f2",ec=O if hit else G,lw=2.6 if hit else 1))
    ax.text(x+1,3.7,"orders_"+m.lower(),ha="center",fontsize=9.5,color=O if hit else G,fontweight="bold" if hit else None)
    ax.text(x+1,2.9,"read" if hit else "skipped",ha="center",fontsize=10,color=O if hit else G)
    if hit: ax.annotate("",xy=(x+1,4.75),xytext=(8,6.1),arrowprops=dict(arrowstyle="->",color=O,lw=2))
ax.text(8,1.2,"Partition pruning: the planner proves five partitions cannot match, so it never opens them",ha="center",fontsize=10.5)
plt.tight_layout(); plt.savefig("ch10_partition.png",dpi=110)
