import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, ax = plt.subplots(figsize=(8, 4.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
def box(x, y, w, h, text, c, fs=8.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", fc=c, ec="none", alpha=.93))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color="white", fontsize=fs, fontweight="bold")
def arr(a, b, label=""):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color="#555", lw=1.2))
    if label: ax.text((a[0] + b[0]) / 2 + .08, (a[1] + b[1]) / 2 + .08, label, fontsize=8, color="#333")
box(3.6, 5.1, 2.8, .7, "Two runs disagree", "#333333")
box(3.3, 3.9, 3.4, .75, "Same seed run twice differs?", B)
arr((5, 5.1), (5, 4.65))
box(0.2, 2.5, 2.7, .95, "NO: seeds are fine.\nCompare against seed noise\n(10 seeds, paired diff)", T, 8)
arr((3.3, 4.2), (1.6, 3.45), "no")
box(3.5, 2.5, 3.0, .95, "YES: diff the five inputs\ncode, data hash, config hash,\nenvironment, hardware", O, 8)
arr((5, 3.9), (5, 3.45), "yes")
box(7.1, 2.5, 2.7, .95, "Still differs after all\nfive match? Hidden RNG,\nthreads, float order", R, 8)
arr((6.5, 2.97), (7.1, 2.97))
box(0.2, 0.6, 2.7, .95, "Noise smaller than gain?\nreport gain. Larger?\nit is not a real gain", T, 8)
arr((1.55, 2.5), (1.55, 1.55))
box(3.5, 0.6, 3.0, .95, "Fix the first input that\nmismatches, pin it, rerun,\nconfirm identical hash", O, 8)
arr((5, 2.5), (5, 1.55))
box(7.1, 0.6, 2.7, .95, "Bisect, then tolerate:\ncompare with allclose,\nnot ==", R, 8)
arr((8.45, 2.5), (8.45, 1.55))
fig.tight_layout(); fig.savefig("ch02d_decision_flow.png", dpi=110)
