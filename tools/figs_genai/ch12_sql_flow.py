"""Text-to-SQL safety flow: each layer can stop a query. Saves ch12_sql_flow.png in the current folder."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
BLUE, ORANGE, TEAL, RED, PURPLE = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.set_xlim(0, 100); ax.set_ylim(0, 50); ax.axis("off")
steps = [("Question", "in plain words", BLUE), ("Model writes\nSQL", "from schema +\nbusiness rules", PURPLE),
         ("Code guard", "one SELECT,\nLIMIT added", ORANGE), ("Database\npermissions", "read-only role,\nauthorizer, timeout", TEAL),
         ("Result", "rows + the SQL\nshown to user", BLUE)]
w, h, y = 15.5, 17, 22
for i, (t, s, c) in enumerate(steps):
    x = 2 + i * 19.5
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.5", fc="white", ec=c, lw=2.5))
    ax.text(x + w / 2, y + h - 4.5, t, ha="center", va="center", fontsize=11.5, fontweight="bold", color=c)
    ax.text(x + w / 2, y + 4.5, s, ha="center", va="center", fontsize=9.5, color="#222")
    if i < len(steps) - 1:
        ax.annotate("", xy=(x + w + 3.5, y + h / 2), xytext=(x + w + 0.4, y + h / 2), arrowprops=dict(arrowstyle="->", lw=2, color="#444"))
for i in (2, 3):
    x = 2 + i * 19.5 + w / 2
    ax.annotate("", xy=(x, 11), xytext=(x, y - 0.5), arrowprops=dict(arrowstyle="->", lw=2, color=RED))
    ax.text(x, 7.5, "reject and log\nthe query", ha="center", va="center", fontsize=9.5, color=RED)
ax.text(50, 46, "Every layer can say no; the prompt alone is not a layer", ha="center", fontsize=12.5, fontweight="bold", color="#222")
fig.tight_layout(); fig.savefig("ch12_sql_flow.png", dpi=110)
