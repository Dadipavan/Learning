import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#c9c9c9"
plt.rcParams.update({"font.size": 14})

fig, ax = plt.subplots(figsize=(8, 5))
cols = {2: ORANGE, 3: TEAL, 5: RED, 7: PURPLE}
spf = {}
for p in (2, 3, 5, 7):
    for m in range(p * p, 50, p):
        spf.setdefault(m, p)
for n in range(1, 50):
    r, c = divmod(n - 1, 7)
    if n == 1:
        fc = GREY
    elif n in spf:
        fc = cols[spf[n]]
    else:
        fc = BLUE
    ax.add_patch(Rectangle((c, 6 - r), 0.92, 0.92, fc=fc, ec="black"))
    ax.text(c + 0.46, 6 - r + 0.46, str(n), ha="center", va="center", color="white" if n != 1 else "black", fontsize=16, fontweight="bold")
ax.set_xlim(0, 7); ax.set_ylim(-0.9, 7.8); ax.axis("off")
ax.set_title("Sieve up to 49: blue = prime, others coloured by the prime that crossed them out", fontsize=12)
ax.text(0, -0.6, "orange: 2   teal: 3   red: 5   purple: 7", fontsize=13)
plt.tight_layout()
plt.savefig("dsa10_sieve.png", dpi=110)
