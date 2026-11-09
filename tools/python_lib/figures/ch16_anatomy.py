import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":15})

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.set_xlim(0,16);ax.set_ylim(0,8.4);ax.axis("off")
# ndarray object
ax.add_patch(Rectangle((0.3,3.2),5.2,4.6,fc="#eef1fc",ec=B,lw=2))
ax.text(2.9,7.3,"ndarray header",ha="center",color=B,fontweight="bold")
for i,t in enumerate(["dtype: int32","shape: (2, 3)","strides: (12, 4)","C-contiguous","data: pointer"]):
    ax.text(0.6,6.5-i*0.75,t,fontsize=12,family="monospace")
# buffer
ax.text(11.0,7.0,"one flat buffer (24 bytes)",ha="center",color=T,fontweight="bold")
cols=[B,B,B,O,O,O]
for i in range(6):
    ax.add_patch(Rectangle((6.6+i*1.5,5.2),1.5,1.2,fc="white",ec=cols[i],lw=2))
    ax.text(7.35+i*1.5,5.8,str(i),ha="center",va="center",fontsize=14)
    ax.text(7.35+i*1.5,4.8,f"+{i*4}",ha="center",fontsize=11,color="#555")
ax.annotate("",xy=(6.6,5.8),xytext=(5.5,5.8),arrowprops=dict(arrowstyle="->",color="#444",lw=2))
ax.text(6.0,6.15,"points to",ha="center",fontsize=11)
# logical view
ax.text(11.0,3.9,"what you see: a 2 x 3 table",ha="center",color=O,fontweight="bold")
for r in range(2):
    for c in range(3):
        ax.add_patch(Rectangle((8.2+c*1.6,1.6-r*1.3+0.3),1.6,1.3,fc="white",ec=[B,O][r],lw=2))
        ax.text(9.0+c*1.6,2.25-r*1.3,str(r*3+c),ha="center",va="center",fontsize=14)
ax.text(8.0,2.2,"row 0",ha="right",fontsize=11);ax.text(8.0,0.9,"row 1",ha="right",fontsize=11)
ax.text(2.9,1.6,"stride 12 = bytes to next row\nstride 4 = bytes to next column",ha="center",fontsize=11.5)
plt.savefig("lib16_anatomy.png",bbox_inches="tight");
