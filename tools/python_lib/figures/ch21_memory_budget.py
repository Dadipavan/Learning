import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
P = 7e9
setups = ["full fp32\n+ Adam", "all bf16\n+ Adam", "LoRA 0.5%\nbf16 base", "inference\nbf16", "inference\n4-bit"]
w = [P*4/1e9, P*2/1e9, (P*0.995*2 + P*0.005*4)/1e9, P*2/1e9, P*0.5/1e9]
g = [P*4/1e9, P*2/1e9, P*0.005*4/1e9, 0, 0]
o = [P*8/1e9, P*4/1e9, P*0.005*8/1e9, 0, 0]
plt.rcParams.update({"font.size": 12})
fig, ax = plt.subplots(figsize=(8, 4.2))
x = np.arange(5)
ax.bar(x, w, color="#2b4fd6", label="weights")
ax.bar(x, g, bottom=w, color="#b84a22", label="gradients")
ax.bar(x, o, bottom=np.array(w) + np.array(g), color="#357a70", label="optimiser state")
for i in range(5):
    t = w[i] + g[i] + o[i]
    ax.text(i, t + 2, f"{t:.1f}", ha="center", fontsize=12, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(setups, fontsize=10)
ax.set_ylabel("GB (7B parameters)"); ax.set_ylim(0, 130); ax.legend(fontsize=11)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig("lib21_memory_budget.png", dpi=110)
