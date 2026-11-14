import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":14,"axes.labelsize":13})
from matplotlib.patches import FancyBboxPatch
fig,ax=plt.subplots(figsize=(9,4.2));ax.set_xlim(0,10);ax.set_ylim(-0.2,4.4);ax.axis("off")
steps=[("1 Understand","Restate it.\nInputs, outputs,\nlimits on n.",B),("2 Examples","Make 2 small ones\nplus an edge case.\nSolve by hand.",T),("3 Brute force","Say the slow way.\nState its Big-O.",O),("4 Optimise","Find the repeated\nwork. Pick a pattern.\nCode, then test.",P)]
for i,(t,d,c) in enumerate(steps):
    x=0.2+i*2.45
    ax.add_patch(FancyBboxPatch((x,1.1),2.1,2.6,boxstyle="round,pad=0.03",fc=c,ec="none"))
    ax.text(x+1.05,3.3,t,ha="center",va="center",color="white",fontsize=13,fontweight="bold")
    ax.text(x+1.05,2.2,d,ha="center",va="center",color="white",fontsize=11.5)
    if i<3: ax.annotate("",xy=(x+2.43,2.4),xytext=(x+2.13,2.4),arrowprops=dict(arrowstyle="->",lw=2.5,color="#333"))
ax.annotate("",xy=(1.2,1.05),xytext=(9.0,1.05),arrowprops=dict(arrowstyle="->",lw=2,color=R,connectionstyle="arc3,rad=-0.12"))
ax.text(5,0.05,"Stuck or wrong? Go back a step. Never skip to coding.",ha="center",fontsize=12.5,color=R)
ax.set_title("The 4-step solve routine")
fig.tight_layout();fig.savefig("dsa1_routine.png",dpi=110)
