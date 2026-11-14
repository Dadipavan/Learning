import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#c9c9c9"
plt.rcParams.update({"font.size": 14})

fig, ax = plt.subplots(figsize=(8, 4.6))
ax.axis("off"); ax.set_xlim(0, 11); ax.set_ylim(0, 7)
rows = [("a = 13", "1101", BLUE), ("b = 6", "0110", ORANGE), ("a & b = 4", "0100", TEAL), ("a | b = 15", "1111", PURPLE), ("a ^ b = 11", "1011", RED)]
for r, (lab, bits, c) in enumerate(rows):
    y = 6 - r * 1.2
    ax.text(0.1, y + 0.4, lab, fontsize=16, va="center")
    for i, b in enumerate(bits):
        x = 5 + i * 1.4
        ax.add_patch(Rectangle((x, y), 1.2, 0.8, fc=c if b == "1" else "white", ec="black", lw=1.5))
        ax.text(x + 0.6, y + 0.4, b, ha="center", va="center", fontsize=18, color="white" if b == "1" else "black", fontweight="bold")
for i, w in enumerate([8, 4, 2, 1]):
    ax.text(5.6 + i * 1.4, 0.3, str(w), ha="center", fontsize=13, color="#444")
ax.text(4.9, 0.3, "place value", ha="right", fontsize=13, color="#444")
plt.tight_layout()
plt.savefig("dsa10_bits.png", dpi=110)
