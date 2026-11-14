import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
N,d,M=50_000_000,768,16
fmt=[("float32",4.0,"#aa2d26"),("float16",2.0,"#b84a22"),("int8",1.0,"#6a2fd0"),("PQ, 96 bytes",96/768,"#357a70")]
fig,ax=plt.subplots(figsize=(8,4.2))
for i,(n,b,c) in enumerate(fmt):
    vec=N*d*b/1e9; links=N*2*M*4/1e9; pay=N*200/1e9
    ax.barh(i,vec,color=c,label="vectors" if i==0 else None); ax.barh(i,links,left=vec,color="#999",label="graph links" if i==0 else None)
    ax.barh(i,pay,left=vec+links,color="#ddd",label="ids and metadata" if i==0 else None)
    ax.text(vec+links+pay+2,i,f"{vec+links+pay:.0f} GB",va="center",fontsize=9,fontweight="bold")
ax.axvline(64*0.7,color="#2b4fd6",ls="--"); ax.text(47,3.0,"usable RAM of one 64 GB machine",color="#2b4fd6",fontsize=8,ha="left")
ax.set_yticks(range(4)); ax.set_yticklabels([f[0] for f in fmt]); ax.invert_yaxis(); ax.set_xlim(0,200)
ax.set_xlabel("memory for 50 million vectors of 768 dimensions, HNSW M=16 (GB)")
ax.set_title("Compression decides how many machines you need"); ax.legend(frameon=False,loc="lower right")
ax.spines[["top","right"]].set_visible(False); fig.tight_layout(); fig.savefig("ch06d_memory.png",dpi=110)
