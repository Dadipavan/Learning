from common import *
from matplotlib.patches import FancyBboxPatch
fig,ax=plt.subplots(figsize=(8,4.2),dpi=110); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,6)
def box(x,y,w,h,t,c,fs=8.5):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.04",fc="white",ec=c,lw=2)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs)
def arr(x1,y1,x2,y2,t=""):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",color="#444",lw=1.4))
    if t: ax.text((x1+x2)/2+0.05,(y1+y2)/2+0.12,t,fontsize=8,color="#444")
box(0.2,4.6,2.2,1.0,"1. What is the\nask and who\ndecides?",BLUE)
box(3.0,4.6,2.2,1.0,"2. Do the numbers\nreconcile? parts\nsum to total?",TEAL)
box(5.8,4.6,2.2,1.0,"3. Which pattern?\n(change, compare,\ntest, funnel...)",ORANGE)
box(8.2,4.6,1.6,1.0,"4. One\nheadline\nwith a number",PURPLE)
arr(2.4,5.1,3.0,5.1); arr(5.2,5.1,5.8,5.1); arr(8.0,5.1,8.2,5.1)
box(0.2,2.4,2.4,1.0,"Not reconciling?\nfix data / definition\nfirst",RED); arr(4.1,4.6,2.0,3.4,"no")
box(3.2,2.4,2.4,1.0,"Is the change\nbigger than noise?\n(interval)",TEAL); arr(6.9,4.6,4.4,3.4)
box(6.2,2.4,2.0,1.0,"5. One chart,\ntitle = message",ORANGE); arr(5.6,2.9,6.2,2.9,"yes / n.a.")
box(8.4,2.4,1.4,1.0,"6. Ask +\ncaveat",PURPLE); arr(8.2,2.9,8.4,2.9)
box(3.2,0.5,3.6,1.0,"Not sure yet? Say \"promising, not proven\"\nand name the cheapest next test",RED); arr(4.4,2.4,4.7,1.5,"no")
ax.text(5,0.1,"Debug when stuck: re-add the parts, change the baseline, shrink the audience, state the opposite",ha="center",fontsize=8,color="#444")
fig.tight_layout(); fig.savefig("ch05d_decision.png")
