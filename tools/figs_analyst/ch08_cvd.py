import matplotlib
matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12,
                     "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlelocation": "left",
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, ORANGE, TEAL, RED, PURPLE, GREY = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0", "#9a9a9a"
from matplotlib.colors import to_rgb

def lin(c):
    c = np.asarray(c, float)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def delin(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)
def to_lab(rgb):
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = (M @ lin(rgb)) / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 216 / 24389, np.cbrt(xyz), (24389 / 27 * xyz + 16) / 116)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])
DEUT = np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]])
PROT = np.array([[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]])
sim = lambda h, M: delin(M @ lin(to_rgb(h)))
grey = lambda h: np.repeat(delin(lin(to_rgb(h)) @ np.array([0.2126, 0.7152, 0.0722])), 3)
def pair_de(a, b):
    return np.linalg.norm(to_lab(a) - to_lab(b))

house = [BLUE, ORANGE, TEAL, RED, PURPLE]
classic = ["#d62728", "#2ca02c", "#1f77b4", "#ff7f0e", "#9467bd"]
conds = [("normal", lambda h: np.array(to_rgb(h))), ("deuteranopia", lambda h: sim(h, DEUT)),
         ("protanopia", lambda h: sim(h, PROT)), ("greyscale", grey)]
fig, ax = plt.subplots(figsize=(8, 5))
y = 0
for pname, pal in [("House palette", house), ("Red/green palette", classic)]:
    for cname, f in conds:
        for j, h in enumerate(pal):
            ax.add_patch(plt.Rectangle((j, -y), 0.94, 0.8, color=np.clip(f(h), 0, 1)))
        ax.text(-0.2, -y + 0.4, f"{pname}: {cname}", ha="right", va="center", fontsize=10.5)
        y += 1
    y += 0.5
ax.set(xlim=(-4.6, 5), ylim=(-y + 0.3, 1)); ax.axis("off")
fig.tight_layout()
fig.savefig("ch08v_cvd.png", dpi=110)
for pname, pal in [("house", house), ("house 3", house[:3]), ("classic", classic)]:
    out = []
    for cname, M in [("normal", None), ("deut", DEUT), ("prot", PROT)]:
        cols = [np.array(to_rgb(h)) if M is None else sim(h, M) for h in pal]
        d = [(np.linalg.norm(to_lab(a) - to_lab(b)), i, j) for i, a in enumerate(cols) for j, b in enumerate(cols) if i < j]
        out.append(f"{cname} {min(d)[0]:.1f}")
    print(f"{pname:<8} smallest pairwise delta-E:", ", ".join(out))
print("(house 3 = blue, orange, teal)")
worst = sorted(((pair_de(sim(a, DEUT), sim(b, DEUT)), na, nb) for (na, a), (nb, b) in
                [(("blue", BLUE), ("orange", ORANGE)), (("blue", BLUE), ("teal", TEAL)), (("orange", ORANGE), ("teal", TEAL)),
                 (("orange", ORANGE), ("red", RED)), (("teal", TEAL), ("red", RED)), (("blue", BLUE), ("purple", PURPLE))]))[:2]
print("house pairs that collide most under deuteranopia:", [(a, b, round(float(d), 1)) for d, a, b in worst])
print("saved")
