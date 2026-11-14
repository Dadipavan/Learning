import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
steps = [("input x", "B,T,E", T, 0.2, 3.6), ("x @ Wq,Wk,Wv", "B,T,E", B, 2.2, 3.6), ("split heads", "B,H,T,D", O, 4.2, 3.6),
         ("Q @ K^T / sqrt(D)", "B,H,T,T", R, 6.2, 3.6), ("softmax + mask", "B,H,T,T", R, 8.1, 3.6),
         ("att @ V", "B,H,T,D", B, 8.1, 1.2), ("merge heads", "B,T,E", O, 6.2, 1.2), ("@ Wo", "B,T,E", B, 4.2, 1.2), ("output", "B,T,E", T, 2.2, 1.2)]
for name, shape, col, x, y in steps:
    ax.add_patch(FancyBboxPatch((x, y), 1.7, 1.4, boxstyle="round,pad=0.05", fc=col, ec="none"))
    ax.text(x + 0.85, y + 0.95, name, ha="center", va="center", color="white", fontsize=9.5, fontweight="bold")
    ax.text(x + 0.85, y + 0.38, shape, ha="center", va="center", color="white", fontsize=11, family="monospace")
def arr(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16, color="#333333", lw=2))
for x in (1.95, 3.95, 5.95, 7.85):
    arr(x, 4.3, x + 0.25, 4.3)
arr(8.95, 3.55, 8.95, 2.65)
for x in (8.05, 6.05, 4.05):
    arr(x, 1.9, x - 0.25, 1.9)
ax.text(5, 5.5, "multi-head self-attention: shape after each step", ha="center", fontsize=13, fontweight="bold")
ax.text(5, 0.35, "B batch, T tokens, E embedding, H heads, D = E / H", ha="center", fontsize=11, color="#444444")
fig.tight_layout(); fig.savefig("lib21_attention_shapes.png", dpi=110)
