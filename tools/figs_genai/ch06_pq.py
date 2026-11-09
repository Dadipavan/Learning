import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig,(a,b)=plt.subplots(1,2,figsize=(8,4.2),gridspec_kw={"width_ratios":[1.15,1]})
a.set_xlim(0,10); a.set_ylim(0,10); a.axis("off")
cols=["#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0","#2b4fd6","#b84a22","#357a70"]
a.text(5,9.4,"One 64-number vector (256 bytes)",ha="center",fontsize=9.5,fontweight="bold")
for i in range(8):
    a.add_patch(Rectangle((0.5+i*1.1,7.6),1.0,1.1,fc=cols[i],alpha=0.85,ec="white"))
    a.text(1.0+i*1.1,8.15,f"p{i+1}",ha="center",va="center",color="white",fontsize=8,fontweight="bold")
a.text(5,6.4,"split into 8 pieces of 8 numbers",ha="center",fontsize=8.5,bbox=dict(fc="white",ec="none",pad=1))
for i in range(8):
    a.annotate("",xy=(1.0+i*1.1,4.9),xytext=(1.0+i*1.1,7.5),arrowprops=dict(arrowstyle="-|>",color=cols[i]))
    a.add_patch(Rectangle((0.5+i*1.1,3.6),1.0,1.2,fc="white",ec=cols[i],lw=2))
    a.text(1.0+i*1.1,4.2,["17","203","5","88","241","9","130","62"][i],ha="center",va="center",fontsize=8.5,color=cols[i],fontweight="bold")
a.text(5,5.6,"each piece replaced by the id of its nearest",ha="center",fontsize=8.5,bbox=dict(fc="white",ec="none",pad=1)); a.text(5,2.9,"of 256 learned patterns (1 byte each)",ha="center",fontsize=8.5)
a.text(5,1.6,"Stored: 8 bytes   (32 times smaller)",ha="center",fontsize=10,fontweight="bold",color="#aa2d26")
labels=["4 bytes","8 bytes","16 bytes"]; pq=[0.181,0.352,0.596]; rs=[0.597,0.833,0.995]
import numpy as np; x=np.arange(3)
b.bar(x-0.19,pq,0.38,color="#b84a22",label="PQ codes only"); b.bar(x+0.19,rs,0.38,color="#2b4fd6",label="PQ + rescore top 100")
for i in range(3):
    b.text(x[i]-0.19,pq[i]+0.015,f"{pq[i]:.2f}",ha="center",fontsize=8); b.text(x[i]+0.19,rs[i]+0.015,f"{rs[i]:.2f}",ha="center",fontsize=8)
b.set_xticks(x); b.set_xticklabels(labels); b.set_ylim(0,1.15); b.set_ylabel("recall@10"); b.set_xlabel("bytes per vector (64 dims)")
b.set_title("Rescoring rescues recall",fontsize=10); b.legend(frameon=False,fontsize=8,loc="upper left"); b.spines[["top","right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch06d_pq.png",dpi=110)
