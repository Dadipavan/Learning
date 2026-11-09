import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
params=7e9
stages=["DDP","ZeRO-1","ZeRO-2","ZeRO-3 / FSDP"]
def parts(stage,n):
    return (params*2/(n if stage>=3 else 1)/1e9, params*2/(n if stage>=2 else 1)/1e9, params*12/(n if stage>=1 else 1)/1e9)
fig,ax=plt.subplots(figsize=(8,4.2))
cols=["#2b4fd6","#357a70","#b84a22"]; labs=["fp16 weights","fp16 gradients","optimizer (fp32 master, m, v)"]
bottom=np.zeros(4)
data=np.array([parts(s,8) for s in range(4)])
for j in range(3):
    ax.bar(stages,data[:,j],bottom=bottom,color=cols[j],label=labs[j]); bottom+=data[:,j]
for i,t in enumerate(bottom): ax.text(i,t+2,f"{t:.0f} GB",ha="center",fontsize=10)
ax.axhline(80,color="#aa2d26",ls="--"); ax.text(3.45,82,"80 GB GPU",color="#aa2d26",ha="right",fontsize=10)
ax.set_ylabel("Model state per GPU (GB)"); ax.set_ylim(0,125); ax.set_title("7B model, 8 GPUs: what each GPU must hold (activations not included)")
ax.legend(loc="upper right",bbox_to_anchor=(1,0.9),fontsize=9); fig.tight_layout(); fig.savefig("ch06_zero_memory.png",dpi=110)
