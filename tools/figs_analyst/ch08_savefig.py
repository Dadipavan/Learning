import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import tempfile, os

fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot([1, 2, 3], [3, 1, 2])
tmp = tempfile.mkdtemp()
for dpi in (72, 110, 300):
    path = os.path.join(tmp, f"chart_{dpi}.png")
    fig.savefig(path, dpi=dpi)
    h, w = plt.imread(path).shape[:2]
    print(f"dpi {dpi:>3}: {w} x {h} pixels  (= 8 x {dpi}, 4.2 x {dpi})")
fig.savefig(os.path.join(tmp, "chart.svg"))
fig.savefig(os.path.join(tmp, "chart.pdf"))
print("formats written:", sorted(f.split(".")[-1] for f in os.listdir(tmp) if not f.startswith("chart_")))
