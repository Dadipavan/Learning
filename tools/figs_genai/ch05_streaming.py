import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
fig, axs = plt.subplots(1, 2, figsize=(8, 4.2), gridspec_kw={"width_ratios": [1.15, 1]})
ax = axs[0]
ttft, rate, n = 0.8, 50, 300
gen = n / rate
ax.barh(1, ttft, color="#b84a22", label="waiting for first token (0.8 s)")
ax.barh(1, gen, left=ttft, color="#2b4fd6", label="generating 300 tokens (6.0 s)")
ax.barh(0, ttft + gen, color="#aa2d26", label="blank screen, then everything at once")
ax.barh(0.0, 0.0)
ax.set_yticks([0, 1]); ax.set_yticklabels(["no streaming\n(user sees nothing)", "streaming\n(user reads from 0.8 s)"], fontsize=8)
ax.axvline(0.8, color="#357a70", ls="--"); ax.text(0.9, 1.45, "first words", color="#357a70", fontsize=8)
ax.axvline(6.8, color="#444444", ls=":"); ax.text(6.7, -0.45, "6.8 s total, same for both", ha="right", fontsize=8)
ax.set_xlabel("seconds"); ax.set_xlim(0, 7.5); ax.set_ylim(-0.6, 1.7)
ax.legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.2))
ax.set_title("Same total, different wait", fontsize=10)
ax = axs[1]
toks = np.array([50, 100, 200, 300, 600, 900])
for r, c in [(30, "#aa2d26"), (50, "#2b4fd6"), (100, "#357a70")]:
    ax.plot(toks, ttft + toks / r, color=c, lw=2, marker="o", ms=3, label=f"{r} tokens/s")
ax.set_xlabel("output tokens"); ax.set_ylabel("total latency (s)")
ax.set_title("Output length drives latency", fontsize=10); ax.legend(frameon=False, fontsize=8)
for a in axs: a.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("ch05d_streaming.png", dpi=110)
