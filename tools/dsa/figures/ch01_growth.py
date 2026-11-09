import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13,"axes.titlesize":14,"axes.labelsize":13})
import math
n=np.arange(1,11)
fig,ax=plt.subplots(figsize=(8,4.6))
series=[("O(1)",np.ones_like(n,float),"#888888"),("O(log n)",np.log2(n),T),("O(n)",n*1.0,B),("O(n log n)",n*np.log2(n),P),("O(n²)",n**2.0,O),("O(2ⁿ)",2.0**n,R),("O(n!)",np.array([math.factorial(int(k)) for k in n],float),"#222222")]
for lab,y,c in series:
    ax.plot(n,y,lw=2.6,color=c,label=lab,marker="o",ms=4)
ax.set_ylim(0,110);ax.set_xlim(1,10)
ax.set_xlabel("input size n");ax.set_ylabel("steps (operations)")
ax.set_title("How fast the work grows as n grows")
ax.legend(loc="upper left",fontsize=12,frameon=False)
ax.grid(alpha=.25)
fig.tight_layout();fig.savefig("dsa1_growth.png",dpi=110)
