import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":15})

fig,axs=plt.subplots(1,2,figsize=(8,4.2),dpi=110)
for ax,(name,order,col) in zip(axs,[("C order (row-major)\nstrides (12, 4)","C",B),("F order (column-major)\nstrides (4, 8)","F",O)]):
    a=np.arange(6).reshape(2,3,order=order) if False else np.arange(6)
    grid=np.zeros((2,3),int)
    k=0
    if order=="C":
        for r in range(2):
            for c in range(3): grid[r,c]=k;k+=1
    else:
        for c in range(3):
            for r in range(2): grid[r,c]=k;k+=1
    ax.imshow(grid,cmap="Blues" if order=="C" else "Oranges",vmin=-3,vmax=8)
    for r in range(2):
        for c in range(3): ax.text(c,r,str(grid[r,c]),ha="center",va="center",fontsize=20,color="black")
    ax.set_title(name,color=col)
    ax.set_xticks(range(3));ax.set_yticks(range(2));ax.set_xlabel("column");ax.set_ylabel("row")
fig.suptitle("Number = position in memory",fontsize=14)
fig.tight_layout();plt.savefig("lib16_layout.png",bbox_inches="tight")
