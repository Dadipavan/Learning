import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams.update({"font.size":13,"axes.titlesize":15,"axes.spines.top":False,"axes.spines.right":False})
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"

left=pd.DataFrame({"k":[1,2,3,4]}); right=pd.DataFrame({"k":[3,4,5,6,7]})
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
res={h:len(left.merge(right,on="k",how=h)) for h in ["inner","left","right","outer"]}
b=ax.bar(list(res),list(res.values()),color=[B,O,T,P])
for r,v in zip(b,res.values()): ax.text(r.get_x()+r.get_width()/2,v+.1,str(v),ha="center",fontsize=14)
ax.set_ylabel("rows in result"); ax.set_title("left keys 1-4, right keys 3-7 (overlap 3,4)"); ax.set_ylim(0,8.5)
plt.savefig("lib17_joins.png",bbox_inches="tight")
