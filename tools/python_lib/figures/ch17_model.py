import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams.update({"font.size":13,"axes.titlesize":15,"axes.spines.top":False,"axes.spines.right":False})
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

from matplotlib.patches import Rectangle
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110); ax.set_xlim(0,10); ax.set_ylim(0,6); ax.axis("off")
cols=[("city",B,["Oslo","Rome","Oslo"]),("sales",O,["10","7","3"]),("paid",T,["True","False","True"])]
ax.text(0.2,5.5,"DataFrame = dict of Series sharing one Index",fontsize=14,weight="bold")
ax.add_patch(Rectangle((0.2,1.2),1.3,3.6,fc="#eeeeee",ec="k")); ax.text(0.85,4.5,"Index",ha="center",weight="bold")
for i,l in enumerate(["0","1","2"]): ax.text(0.85,3.7-i*1.0,l,ha="center",va="center")
for j,(n,c,v) in enumerate(cols):
    x=1.8+j*2.0
    ax.add_patch(Rectangle((x,1.2),1.8,3.6,fc="white",ec=c,lw=2.5)); ax.text(x+0.9,4.5,n,ha="center",weight="bold",color=c)
    for i,t in enumerate(v): ax.text(x+0.9,3.7-i*1.0,t,ha="center",va="center")
    ax.text(x+0.9,0.75,["dtype str","dtype int64","dtype bool"][j],ha="center",color=c,fontsize=12)
ax.annotate("one column = one Series",xy=(4.8,4.9),xytext=(6.3,4.5),arrowprops=dict(arrowstyle="->"),fontsize=12)
ax.text(8.2,3.2,"axis=0\nrows go down",fontsize=12,color=R); ax.text(8.2,2.0,"axis=1\ncolumns go across",fontsize=12,color=P)
plt.savefig("lib17_model.png",bbox_inches="tight")
