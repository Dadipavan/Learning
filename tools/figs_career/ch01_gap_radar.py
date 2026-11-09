import numpy as np
from common import *
skills=["SQL","Python","Pipelines\n(Airflow)","Cloud","Data\nmodelling","System\ndesign"]
target=[4,4,3,3,3,3]; now=[2,2,1,2,1,2]
gap=[t-n for t,n in zip(target,now)]
print("gap points",sum(gap),"hours",sum(gap)*20)
ang=np.linspace(0,2*np.pi,len(skills),endpoint=False).tolist(); ang+=ang[:1]
fig=plt.figure(figsize=(7,5),dpi=110); ax=fig.add_subplot(111,polar=True)
for v,c,l in ((target,BLUE,"Target: Data Engineer (junior)"),(now,ORANGE,"You today (IT support, 6 years)")):
    w=v+v[:1]; ax.plot(ang,w,color=c,lw=2,label=l); ax.fill(ang,w,color=c,alpha=0.15)
ax.set_xticks(ang[:-1]); ax.set_xticklabels(skills,fontsize=10); ax.set_ylim(0,5); ax.set_yticks([1,2,3,4,5]); ax.tick_params(axis="y",labelsize=8)
ax.legend(loc="upper right",bbox_to_anchor=(1.35,1.12),fontsize=9,frameon=False)
fig.tight_layout(); fig.savefig("ch01_gap_radar.png")
