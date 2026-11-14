import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
def box(x, y, w, h, t, c, fs=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc="white", ec=c, lw=2.5))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs)
def arr(a, b, t=None):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", lw=2))
box(0.1, 2.4, 2.0, 1.3, "Client\nPOST /predict\nJSON body", B, 11)
box(2.9, 2.4, 2.3, 1.3, "Validation\ntypes, ranges", O, 11)
box(6.0, 2.4, 2.3, 1.3, "Handler\nmodel.predict", T, 11)
box(9.1, 2.4, 2.6, 1.3, "Response\n200 + JSON", P, 11)
box(2.9, 0.3, 2.3, 1.1, "422 error\nlist of problems", R, 11)
box(6.0, 4.5, 2.3, 1.1, "Model loaded\nonce at startup", T, 11)
arr((2.15, 3.05), (2.85, 3.05)); arr((5.25, 3.05), (5.95, 3.05)); arr((8.35, 3.05), (9.05, 3.05))
arr((4.05, 2.35), (4.05, 1.45)); arr((7.15, 4.45), (7.15, 3.75))
fig.tight_layout(); fig.savefig("lib23_api_flow.png")
