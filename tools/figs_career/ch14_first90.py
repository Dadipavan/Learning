from common import *
rows=[("Listen and learn",0,30,BLUE),("Get access, read code and dashboards",0,14,BLUE),("Meet 10 people (1:1)",7,30,BLUE),("First small win shipped",14,45,TEAL),("Own one recurring task",30,60,TEAL),("Document what you found",30,75,TEAL),("Propose one improvement with numbers",60,90,ORANGE),("Review with manager, set next goals",80,90,ORANGE)]
fig,ax=plt.subplots(figsize=(8.5,4.4),dpi=110)
for i,(n,s,e,c) in enumerate(rows): ax.barh(i,e-s,left=s,color=c,height=0.55)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows],fontsize=9); ax.invert_yaxis()
for d in (30,60,90): ax.axvline(d,color=GREY,ls="--",lw=1)
ax.set_xlabel("days since joining"); ax.set_xlim(0,95); clean(ax)
fig.tight_layout(); fig.savefig("ch14_first90.png")
