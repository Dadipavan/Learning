import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":14,"axes.labelsize":13})
from matplotlib.patches import FancyBboxPatch
fig,(a,b)=plt.subplots(2,1,figsize=(9,6),gridspec_kw={"height_ratios":[1.5,1]})
names=["Big-O\nToolkit","Hashing","Pointers\nWindow","Sort\nBinary","Lists\nStacks","Recursion","Trees\nHeaps","Graphs","DP","Greedy\nBits","Design","Mock\nPlan"]
cols=[B,B,B,T,T,O,O,O,P,P,R,R]
for i,(nm,c) in enumerate(zip(names,cols)):
    r,cc=divmod(i,6)
    a.add_patch(FancyBboxPatch((cc*1.65+0.05,1-r*1.15),1.5,0.9,boxstyle="round,pad=0.02",fc=c,ec="none"))
    a.text(cc*1.65+0.8,1.62-r*1.15,f"Week {i+1}",ha="center",va="center",color="white",fontsize=11,fontweight="bold")
    a.text(cc*1.65+0.8,1.25-r*1.15,nm,ha="center",va="center",color="white",fontsize=11)
a.set_xlim(0,10);a.set_ylim(-0.3,2.2);a.axis("off")
a.set_title("The 12-week plan: one chapter per week")
days=[0,1,3,7,14,30]
b.hlines(0,-1,32,color="#999",lw=2)
for d in days:
    b.plot(d,0,"o",ms=15,color=T if d else B)
    b.text(d,0.3+(0.25 if d==1 else 0),"solve" if d==0 else f"day {d}",ha="center",fontsize=12)
b.set_xlim(-2,33);b.set_ylim(-0.6,0.9);b.set_yticks([]);b.set_xlabel("days after you first solve a problem")
b.set_title("Spaced repetition: re-solve from a blank page")
for s in ("top","right","left"):b.spines[s].set_visible(False)
fig.tight_layout();fig.savefig("dsa1_roadmap.png",dpi=110)
