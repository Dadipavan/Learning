import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
T = [512,1024,2048,4096,8192,16384,32768]
def kv(h,t): return 2*32*h*128*t*2/2**30
fig, ax = plt.subplots(figsize=(8,4.2))
for h,c,n in [(32,"#b84a22","MHA, 32 KV heads"),(8,"#2b4fd6","GQA, 8 KV heads"),(1,"#357a70","MQA, 1 KV head")]:
    ax.plot(T,[kv(h,t) for t in T],marker="o",color=c,lw=2,label=n)
ax.axhline(13.04,color="#444",ls="--"); ax.text(560,14,"7B fp16 weights: 13.0 GiB",fontsize=11)
ax.set_xscale("log",base=2); ax.set_yscale("log")
ax.set_xlabel("context length (tokens)",fontsize=12); ax.set_ylabel("KV cache per sequence (GiB)",fontsize=12)
ax.set_title("KV cache size, 32 layers, head dim 128, fp16",fontsize=13)
ax.tick_params(labelsize=11); ax.grid(alpha=.3); ax.legend(fontsize=11)
fig.tight_layout(); fig.savefig("kv_cache_growth.png",dpi=110)
