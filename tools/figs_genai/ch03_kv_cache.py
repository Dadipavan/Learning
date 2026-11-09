import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
def kv_gb(layers, kv_heads, head_dim, seq, bytes_=2):
    return 2 * layers * kv_heads * head_dim * seq * bytes_ / 1e9
seq = np.array([1, 2, 4, 8, 16, 32, 64, 128]) * 1024
fig, ax = plt.subplots(figsize=(8, 4.2))
for lab, args, col in [("70B, 8 KV heads (GQA)", (80, 8, 128), "#b84a22"),
                       ("7B, 32 KV heads (full MHA)", (32, 32, 128), "#2b4fd6"),
                       ("7B, 8 KV heads (GQA)", (32, 8, 128), "#357a70")]:
    ax.plot(seq / 1024, [kv_gb(*args, s) for s in seq], marker="o", color=col, lw=2, label=lab)
ax.axhline(80, color="#aa2d26", ls="--"); ax.text(1.1, 84, "one 80 GB GPU", color="#aa2d26", fontsize=9)
ax.set_xscale("log", base=2); ax.set_yscale("log")
ax.set_xticks(seq / 1024); ax.set_xticklabels([f"{int(s/1024)}k" for s in seq])
ax.set_xlabel("context length (tokens, one request)"); ax.set_ylabel("KV cache (GB, fp16)")
ax.set_title("KV cache grows linearly with context")
ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch03_kv_cache.png", dpi=110)
