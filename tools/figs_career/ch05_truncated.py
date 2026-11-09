from common import *
m=["Jan","Feb","Mar"]; v=[295,282,284]
fig,(a,b)=plt.subplots(1,2,figsize=(8,4.2),dpi=110)
for ax,base,t,c in ((a,0,"Baseline 0: honest",TEAL),(b,270,"Baseline 270: exaggerated",RED)):
    ax.bar(m,[x-base for x in v],bottom=base,color=c,width=0.55)
    ax.set_ylim(base,305); ax.set_title(t,fontsize=10,color=c); clean(ax)
    for i,x in enumerate(v): ax.text(i,x+2,str(x),ha="center",fontsize=9)
a.set_ylabel("total sales, lakh rupees",fontsize=9)
a.set_xlabel("Mar bar is 96% as tall as Jan",fontsize=9)
b.set_xlabel("Mar bar looks 56% as tall as Jan",fontsize=9)
fig.suptitle("Same data (295, 282, 284), two impressions",fontsize=11,fontweight="bold")
fig.tight_layout(); fig.savefig("ch05d_truncated.png")
