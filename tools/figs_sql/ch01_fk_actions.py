import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig,axs=plt.subplots(1,3,figsize=(8,4.2))
titles=[("RESTRICT / NO ACTION",R,"DELETE is refused"),("ON DELETE CASCADE",O,"children vanish too"),("ON DELETE SET NULL",T,"children kept, link blanked")]
for ax,(t,c,sub) in zip(axs,titles):
    ax.axis("off"); ax.set_xlim(0,4); ax.set_ylim(0,8); ax.set_title(t,fontsize=8.5,color=c,weight="bold")
    ax.text(2,7.4,"delete dept 10",ha="center",fontsize=9,weight="bold")
    ax.add_patch(FancyBboxPatch((0.5,5.6),3,1,boxstyle="round,pad=0.05",fc="white",ec=c if t[0]!="R" else R,lw=2))
    ax.text(2,6.1,"dept 10 Testing",ha="center",va="center",fontsize=8.5)
    rows=[("Asha",10),("Meena",10),("Ravi",20)]
    for i,(n,d) in enumerate(rows):
        y=3.9-i*1.3
        if t.startswith("RESTRICT"): txt=f"{n}  dept {d}"; col="black"; ec="#777"
        elif "CASCADE" in t:
            if d==10: txt=f"{n}  (deleted)"; col="#aaa"; ec="#ccc"
            else: txt=f"{n}  dept {d}"; col="black"; ec="#777"
        else:
            txt=f"{n}  dept "+("NULL" if d==10 else str(d)); col="black"; ec="#777"
        ax.add_patch(FancyBboxPatch((0.5,y),3,0.9,boxstyle="round,pad=0.03",fc="white",ec=ec,lw=1.4,ls="--" if "deleted" in txt else "-"))
        ax.text(2,y+0.45,txt,ha="center",va="center",fontsize=8.5,color=col)
    ax.text(2,0.3,sub,ha="center",fontsize=8.5,color=c)
plt.tight_layout(); plt.savefig("ch01d_fk_actions.png",dpi=110)
