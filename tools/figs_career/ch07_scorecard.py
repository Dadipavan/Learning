import numpy as np
from common import *
crit=["Structure","Evidence","Numbers","Delivery"]
scores={"Structure":[2,3,3,4,4],"Evidence":[2,2,3,3,4],"Numbers":[1,2,2,3,4],"Delivery":[2,3,3,3,4]}
cols=[BLUE,ORANGE,TEAL,PURPLE]
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
for c,col in zip(crit,cols): ax.plot(range(1,6),scores[c],marker="o",color=col,lw=2,label=c)
tot=[sum(scores[c][i] for c in crit) for i in range(5)]
print(tot,[t/16 for t in tot])
ax.set_xticks(range(1,6)); ax.set_xlabel("mock interview number"); ax.set_ylabel("score (1 to 5)"); ax.set_ylim(0,5.3); clean(ax)
ax.legend(frameon=False,ncol=4,loc="upper left")
for i,t in enumerate(tot): ax.text(i+1,0.2,f"total {t}/20",ha="center",fontsize=9)
fig.tight_layout(); fig.savefig("ch07_scorecard.png")
