import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams.update({"font.size":13,"axes.titlesize":15,"axes.spines.top":False,"axes.spines.right":False})
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

from matplotlib.patches import FancyBboxPatch
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110); ax.set_xlim(0,12); ax.set_ylim(0,6); ax.axis("off")
def box(x,y,w,h,t,c):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05",fc="white",ec=c,lw=2.5)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=12)
box(0.2,2.3,2.4,1.6,"all rows\nA,B,A,C,B,A",B)
for i,(k,c) in enumerate([("A: 3 rows",O),("B: 2 rows",T),("C: 1 row",P)]):
    y=4.3-i*1.9; box(4.2,y,2.2,1.1,k,c); box(8.0,y,1.6,1.1,["sum","sum","sum"][i],c)
    ax.annotate("",xy=(4.1,y+.55),xytext=(2.8,3.1),arrowprops=dict(arrowstyle="->"))
    ax.annotate("",xy=(7.9,y+.55),xytext=(6.5,y+.55),arrowprops=dict(arrowstyle="->"))
box(10.2,2.3,1.6,1.6,"one row\nper key",R)
for y in (4.85,2.95,1.05): ax.annotate("",xy=(10.1,3.1),xytext=(9.7,y),arrowprops=dict(arrowstyle="->"))
ax.text(1.4,1.7,"SPLIT",ha="center",weight="bold",color=B,fontsize=14); ax.text(5.3,0.1,"APPLY",ha="center",weight="bold",color=O,fontsize=14); ax.text(11,1.7,"COMBINE",ha="center",weight="bold",color=R,fontsize=14)
plt.savefig("lib17_splitapply.png",bbox_inches="tight")
