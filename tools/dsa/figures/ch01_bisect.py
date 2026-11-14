import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":14,"axes.labelsize":13})
from matplotlib.patches import Rectangle
a=[2,5,8,12,16,23,38,56,72,91]
steps=[(0,9,4,"16 < 23: throw away the left half, lo = mid+1"),(5,9,7,"56 > 23: throw away the right half, hi = mid-1"),(5,6,5,"23 == 23: found at index 5")]
fig,axs=plt.subplots(3,1,figsize=(8.6,6.2))
for ax,(lo,hi,mid,msg) in zip(axs,steps):
    ax.set_xlim(-0.6,10.4);ax.set_ylim(-1.2,2.2);ax.axis("off")
    for i,v in enumerate(a):
        inr=lo<=i<=hi
        ax.add_patch(Rectangle((i,0),0.95,0.9,fc=(B if inr else "#d5d5d5"),ec="white",lw=2))
        ax.text(i+0.47,0.45,str(v),ha="center",va="center",color="white" if inr else "#777",fontsize=14,fontweight="bold")
        ax.text(i+0.47,-0.2,str(i),ha="center",va="center",fontsize=10,color="#555")
    for nm,idx,c,dy in (("lo",lo,T,0),("mid",mid,O,0),("hi",hi,R,0)):
        off={"lo":-0.18,"mid":0.47,"hi":1.1}[nm]
        ax.annotate(nm,xy=(idx+0.47,0.92),xytext=(idx+0.47+(-0.2 if nm=="lo" else 0.2 if nm=="hi" else 0),1.45+(0.55 if (nm=="mid" and lo==mid) else 0)),ha="center",color=c,fontsize=13,fontweight="bold",arrowprops=dict(arrowstyle="->",color=c,lw=2.2))
    ax.text(-0.5,-0.75,msg,fontsize=12,color="#222")
fig.suptitle("Binary search for 23: each step halves the search range",fontsize=14)
fig.tight_layout(rect=(0,0,1,0.96));fig.savefig("dsa1_bisect.png",dpi=110)
