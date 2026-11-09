from common import *
import numpy as np
sc=[("Test 1: 400/10,000 vs 450/10,000",0.005,0.002853),("Test 2: 80/2,000 vs 96/2,000",0.008,0.006484),("Test 3: 4,000/100,000 vs 4,500/100,000",0.005,0.000902)]
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
for i,(t,d,se) in enumerate(sc[::-1]):
    lo,hi=d-1.96*se,d+1.96*se; c=TEAL if lo>0 else ORANGE
    ax.plot([lo*100,hi*100],[i,i],color=c,lw=4); ax.plot(d*100,i,"o",color="white",mec=c,ms=8,mew=2)
    ax.text(hi*100+0.1,i,f"{lo*100:+.2f} to {hi*100:+.2f} points",va="center",fontsize=8.5)
ax.axvline(0,color="#444",ls="--"); ax.set_yticks(range(3)); ax.set_yticklabels([s[0] for s in sc[::-1]],fontsize=8)
ax.set_xlim(-1.5,3.3); ax.set_xlabel("lift in conversion rate, percentage points (95% interval)"); clean(ax)
ax.set_title("Same 0.5 to 0.8 point lift: the interval, not the point, decides",fontsize=10,fontweight="bold",loc="left")
ax.set_ylim(-0.5,2.5); ax.text(0.05,2.3,"orange: interval crosses 0, not yet proven",fontsize=8.5,color=ORANGE); ax.text(0.05,2.1,"teal: whole interval above 0",fontsize=8.5,color=TEAL)
fig.tight_layout(); fig.savefig("ch05d_ab_interval.png")
