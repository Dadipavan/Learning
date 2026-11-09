import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
layers = [("FROM python:3.12-slim", "changes rarely", B), ("pip install -r requirements.txt", "changes when deps change", T),
          ("COPY src/ ./src", "changes every commit", O), ("CMD uvicorn ...", "metadata only", P)]
for i, (t, n, c) in enumerate(layers):
    y = 0.4 + (3 - i) * 1.3
    ax.barh(y + 0.5, 6.3, left=0.3, height=1.05, color=c, alpha=0.9)
    ax.text(0.5, y + 0.5, t, va="center", color="white", fontsize=12, fontweight="bold")
    ax.text(6.9, y + 0.5, n, va="center", fontsize=12)
ax.annotate("", xy=(11.6, 0.6), xytext=(11.6, 5.3), arrowprops=dict(arrowstyle="->", lw=2.5, color=R))
ax.text(11.4, 3.0, "a changed layer rebuilds all lines below it", rotation=90, va="center", ha="right", fontsize=11, color=R)
ax.set_title("Order Dockerfile lines from stable to volatile", fontsize=14)
fig.tight_layout(); fig.savefig("lib23_docker_layers.png")
