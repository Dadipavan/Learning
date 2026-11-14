from common import *
import numpy as np
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
groups=["Mobile","Desktop","Overall"]; A=[8.0,17.0,15.2]; B=[9.0,18.0,10.8]
x=np.arange(3); w=0.36
ax.bar(x-w/2,A,w,color=BLUE,label="Variant A"); ax.bar(x+w/2,B,w,color=ORANGE,label="Variant B")
for i in range(3):
    ax.text(i-w/2,A[i]+0.3,f"{A[i]}%",ha="center",fontsize=9); ax.text(i+w/2,B[i]+0.3,f"{B[i]}%",ha="center",fontsize=9)
ax.set_xticks(x); ax.set_xticklabels(groups); ax.set_ylabel("conversion rate (%)"); ax.set_ylim(0,21); clean(ax); ax.legend(frameon=False)
ax.text(0,12,"A got 20% mobile traffic,\nB got 80% mobile",ha="center",fontsize=8.5,color="#444")
ax.set_title("Simpson's paradox: B wins in each segment, A wins overall (traffic mix)",fontsize=10,fontweight="bold",loc="left")
fig.tight_layout(); fig.savefig("ch05d_simpson.png")
