import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
st = [("1", "Frame", "questions,\nmetrics"), ("2", "Engineer", "schema, load,\nchecks"), ("3", "Clean", "duplicates,\nmissing, types"),
      ("4", "Analyse", "SQL, pandas,\nExcel, DAX"), ("5", "Test", "intervals,\nA/B, forecast"), ("6", "Model", "features,\nvalidation"),
      ("7", "GenAI", "deep nets,\nretrieval"), ("8", "Deliver", "package,\nmonitor, memo")]
cols = ["#2b4fd6", "#6a2fd0", "#357a70", "#b84a22", "#aa2d26", "#2b4fd6", "#6a2fd0", "#357a70"]
fig, ax = plt.subplots(figsize=(11, 3.6)); ax.set_xlim(0, 11); ax.set_ylim(-0.2, 3.6); ax.axis("off")
for i, ((n, t, s), c) in enumerate(zip(st, cols)):
    x = 0.15 + i * 1.34
    ax.add_patch(FancyBboxPatch((x, 1.2), 1.1, 1.7, boxstyle="round,pad=0.03", fc=c, ec="none"))
    ax.text(x + .55, 2.6, n, color="white", ha="center", fontsize=13, fontweight="bold")
    ax.text(x + .55, 2.2, t, color="white", ha="center", fontsize=9, fontweight="bold")
    ax.text(x + .55, 1.6, s, color="white", ha="center", fontsize=7.5)
    if i < 7: ax.add_patch(FancyArrowPatch((x + 1.13, 2.05), (x + 1.31, 2.05), arrowstyle="-|>", mutation_scale=10, color="#12182b"))
ax.add_patch(FancyArrowPatch((10.5, 1.15), (0.7, 1.15), connectionstyle="arc3,rad=-0.18", arrowstyle="-|>", mutation_scale=12, color="#555", ls="--"))
ax.text(5.6, 0.0, "monitoring and surprises send you back: new questions, new cleaning rules, retraining", ha="center", fontsize=9, color="#333")
ax.text(5.5, 3.4, "One dataset, eight stages", ha="center", fontsize=12, fontweight="bold")
fig.savefig("lifecycle.png", dpi=110, bbox_inches="tight")
