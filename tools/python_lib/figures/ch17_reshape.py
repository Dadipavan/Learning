import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams.update({"font.size":13,"axes.titlesize":15,"axes.spines.top":False,"axes.spines.right":False})
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

from matplotlib.patches import Rectangle
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110); ax.set_xlim(0,12); ax.set_ylim(0,6); ax.axis("off")
def grid(x,y,hdr,rows,c,w=1.1):
    for j,h in enumerate(hdr): ax.add_patch(Rectangle((x+j*w,y),w,.6,fc=c,ec="k")); ax.text(x+j*w+w/2,y+.3,h,ha="center",va="center",color="white",fontsize=11,weight="bold")
    for i,r in enumerate(rows):
        for j,v in enumerate(r): ax.add_patch(Rectangle((x+j*w,y-(i+1)*.6),w,.6,fc="white",ec="k")); ax.text(x+j*w+w/2,y-(i+1)*.6+.3,v,ha="center",va="center",fontsize=11)
ax.text(0.2,5.6,"wide",weight="bold",fontsize=14,color=B); ax.text(7,5.6,"long",weight="bold",fontsize=14,color=O)
grid(0.2,4.2,["id","Q1","Q2"],[["a","5","7"],["b","3","4"]],B)
grid(7,4.2,["id","qtr","val"],[["a","Q1","5"],["a","Q2","7"],["b","Q1","3"],["b","Q2","4"]],O)
ax.annotate("",xy=(6.8,3.4),xytext=(3.9,3.4),arrowprops=dict(arrowstyle="->",lw=2,color=R)); ax.text(5.35,3.6,"melt",ha="center",fontsize=14,color=R)
ax.annotate("",xy=(3.9,2.4),xytext=(6.8,2.4),arrowprops=dict(arrowstyle="->",lw=2,color=P)); ax.text(5.35,2.6,"pivot",ha="center",fontsize=14,color=P)
ax.text(0.2,1.0,"melt: columns become rows.  pivot: rows become columns.",fontsize=12)
plt.savefig("lib17_reshape.png",bbox_inches="tight")
