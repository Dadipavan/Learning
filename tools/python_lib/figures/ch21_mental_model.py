import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

C = ["#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"]
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

def box(x, y, w, h, text, col):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=col, ec="none", alpha=0.92))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color="white", fontsize=11, fontweight="bold")

def arrow(x1, y1, x2, y2, col="#333333", style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=16, color=col, lw=2))

top = [("DataLoader\nbatches", C[0]), ("Model\nparameters", C[2]), ("Loss\none number", C[1]), ("backward()\ngradients", C[3]), ("Optimiser\nstep()", C[4])]
for i, (t, c) in enumerate(top):
    x = 0.2 + i * 1.95
    box(x, 3.7, 1.55, 1.4, t, c)
    if i < 4:
        arrow(x + 1.6, 4.4, x + 1.93, 4.4)
arrow(0.2 + 4 * 1.95 + 0.7, 3.65, 0.2 + 1.95 + 0.7, 3.65 - 0.0, col="#555555")
ax.text(5.0, 3.2, "update parameters, then next batch", ha="center", fontsize=11, color="#555555")
ax.text(0.2, 5.6, "Training loop", fontsize=13, fontweight="bold")
ax.text(0.2, 2.45, "GenAI request path", fontsize=13, fontweight="bold")
bot = [("Tokenise\ntext to ids", C[0]), ("Embed\nvectors", C[2]), ("Search\ntop-k", C[1]), ("LLM call\nretry, stream", C[3]), ("Validate\nJSON, eval", C[4])]
for i, (t, c) in enumerate(bot):
    x = 0.2 + i * 1.95
    box(x, 0.5, 1.55, 1.4, t, c)
    if i < 4:
        arrow(x + 1.6, 1.2, x + 1.93, 1.2)
fig.tight_layout()
fig.savefig("lib21_mental_model.png", dpi=110)
