from common import *
lab=["Jan total","North","West","South","Mar total"]; ch=[295,10,4,-25,284]
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
run=295
ax.bar(0,295,color=GREY,width=0.6); ax.text(0,297,"295",ha="center",fontsize=9)
for i,(l,c) in enumerate(zip(lab[1:4],ch[1:4]),1):
    bottom=run if c>0 else run+c
    ax.bar(i,abs(c),bottom=bottom,color=TEAL if c>0 else RED,width=0.6)
    ax.text(i,max(run,run+c)+2,f"{c:+d}",ha="center",fontsize=9,fontweight="bold")
    run+=c
ax.bar(4,284,color=BLUE,width=0.6); ax.text(4,286,"284",ha="center",fontsize=9)
ax.set_xticks(range(5)); ax.set_xticklabels(lab); ax.set_ylim(250,320); clean(ax)
ax.set_ylabel("lakh rupees per month (axis starts at 250)",fontsize=8)
ax.set_title("South explains more than the whole fall: -25 against +14 elsewhere",fontsize=10,fontweight="bold",loc="left")
fig.tight_layout(); fig.savefig("ch05d_waterfall.png")
