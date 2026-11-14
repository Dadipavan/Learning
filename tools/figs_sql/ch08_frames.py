import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
B,O,T,G="#2b4fd6","#b84a22","#357a70","#bbbbbb"
rows=[(1,1,10),(2,2,20),(3,2,30),(4,2,40),(5,4,50),(6,5,60),(7,7,70)]
panels=[("ROWS BETWEEN 1 PRECEDING AND CURRENT ROW",{4,5},"sum = 40 + 50 = 90"),
        ("RANGE BETWEEN 1 PRECEDING AND CURRENT ROW",{5},"d must be 3 or 4, so only row 5: sum = 50"),
        ("GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW",{2,3,4,5},"previous group (d = 2) plus current: 20+30+40+50 = 140")]
fig,axs=plt.subplots(3,1,figsize=(8,5.2))
for ax,(title,inframe,res) in zip(axs,panels):
    ax.set_xlim(0,7.2); ax.set_ylim(-0.1,1.25); ax.axis("off")
    ax.set_title(title+"   (current row: id 5)",fontsize=9.5,loc="left",color="#222")
    for i,(rid,d,v) in enumerate(rows):
        hit=rid in inframe
        ax.add_patch(Rectangle((i,0.1),0.92,0.85,fc="#dfe8ff" if hit else "white",ec=O if rid==5 else (B if hit else G),lw=2.4 if rid==5 else 1.2))
        ax.text(i+.46,.72,"id %d"%rid,ha="center",fontsize=8.5)
        ax.text(i+.46,.45,"d=%d"%d,ha="center",fontsize=8.5,color=T)
        ax.text(i+.46,.2,"v=%d"%v,ha="center",fontsize=8.5)
    ax.text(7.2,1.08,res,ha="right",fontsize=9,color=O)
plt.tight_layout(); plt.savefig("ch08_frames.png",dpi=110)
