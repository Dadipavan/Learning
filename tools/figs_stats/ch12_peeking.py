import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, Rd, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
K = 5; looks = np.arange(1, K + 1)
for seed in range(1000):
    rng = np.random.default_rng(seed)
    S = np.cumsum(rng.standard_normal((8, K)), axis=1); z = S / np.sqrt(looks)
    cross = (np.abs(z) > 1.96).any(axis=1).sum()
    if cross >= 2 and not (np.abs(z) > 2.033 * np.sqrt(K / looks)).any(): break
fig, ax = plt.subplots(figsize=(9.5, 4.4))
for r in z: ax.plot(looks, r, color="#d08a1a" if (np.abs(r) > 1.96).any() else "#999999", lw=1.4, marker="o", ms=3)
ax.plot(looks, np.full(K, 1.96), color=Rd, lw=2, label="naive 1.96 at every look")
ax.plot(looks, np.full(K, 2.413), color=P, lw=2, ls="--", label="Pocock 2.41")
ax.plot(looks, 2.033 * np.sqrt(K / looks), color=T, lw=2.5, label="O'Brien-Fleming")
for l, v in zip(looks, 2.033 * np.sqrt(K / looks)): ax.text(l + .08, min(v, 3.4) + .08, f"{v:.2f}", ha="center", fontsize=8, color=T)
ax.plot(looks, -np.full(K, 1.96), color=Rd, lw=2); ax.plot(looks, -np.full(K, 2.413), color=P, lw=2, ls="--"); ax.plot(looks, -2.033 * np.sqrt(K / looks), color=T, lw=2.5)
ax.set_ylim(-3.6, 3.6); ax.set_xticks(looks); ax.set_xlabel("look number (equally spaced in sample size)")
ax.set_ylabel("z statistic of an A/A test"); ax.set_title("Eight A/A tests: orange ones would look like wins at 1.96")
ax.legend(frameon=False, loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=9)
plt.tight_layout(); plt.savefig("ch12_peeking.png", dpi=110)
