import numpy as np
from common import *
names=["A: IT services","B: GCC","C: Startup"]
fixed=[14,20,17]; var=[1,2,0]; join=[0,2,0]; esop=[0,0,2]
print([f+v+j+e for f,v,j,e in zip(fixed,var,join,esop)])
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110); bot=np.zeros(3)
for vals,l,c in ((fixed,"Fixed pay",BLUE),(var,"Expected variable",TEAL),(join,"Joining bonus (year 1 only)",ORANGE),(esop,"ESOP, risk-adjusted per year",PURPLE)):
    ax.bar(names,vals,bottom=bot,color=c,label=l); bot+=np.array(vals)
for i,t in enumerate(bot): ax.text(i,t+0.4,f"{t:.0f} lakh",ha="center",fontsize=10)
ax.set_ylabel("year-1 value, lakh per year (illustrative)"); ax.set_ylim(0,28); clean(ax); ax.legend(frameon=False,loc="upper left",fontsize=9)
fig.tight_layout(); fig.savefig("ch12_offer_compare.png")
