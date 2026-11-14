from common import *
from matplotlib.patches import FancyBboxPatch
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,5)
steps=[("Raw table","9 numbers\n3 regions x 3 months",GREY),("Compute","percent change,\ncontribution",BLUE),("One insight","South -31.2%\nrest growing",ORANGE),("One chart","title = message\nSouth highlighted",TEAL),("Recommendation","check South data,\nstock, price",PURPLE)]
w=1.7
for i,(t,s,c) in enumerate(steps):
    x=0.2+i*1.95
    ax.add_patch(FancyBboxPatch((x,2.0),w,1.6,boxstyle="round,pad=0.05",fc="white",ec=c,lw=2))
    ax.text(x+w/2,3.2,t,ha="center",va="center",fontsize=9,fontweight="bold",color=c)
    ax.text(x+w/2,2.55,s,ha="center",va="center",fontsize=8.5)
    if i<4: ax.annotate("",xy=(x+w+0.2,2.8),xytext=(x+w+0.02,2.8),arrowprops=dict(arrowstyle="->",color="#444",lw=1.5))
ax.text(5,4.5,"Your job is to shrink: nine numbers become one sentence and one action",ha="center",fontsize=11,fontweight="bold")
ax.text(5,1.2,"Check at every arrow: do the parts add up to the total? is the baseline fair?",ha="center",fontsize=9.5,color="#444")
ax.text(5,0.6,"Then ask: who decides, how much time do they have, what do I want them to do?",ha="center",fontsize=9.5,color="#444")
fig.tight_layout(); fig.savefig("ch05d_flow.png")
