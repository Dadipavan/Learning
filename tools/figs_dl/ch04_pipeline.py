import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig, ax = plt.subplots(figsize=(8,4.2)); ax.set_xlim(0,100); ax.set_ylim(0,60); ax.axis("off")
def box(x,y,w,h,txt,c):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.4,rounding_size=1.5",fc="white",ec=c,lw=2))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=9.5,color="black")
def arr(x1,y1,x2,y2,c="#444"):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",color=c,lw=1.8))
def bug(x,y,n):
    ax.add_patch(plt.Circle((x,y),2.1,fc=R,ec="none")); ax.text(x,y,str(n),color="white",ha="center",va="center",fontsize=10,fontweight="bold")
box(2,40,16,12,"Data\nfiles",B); box(24,40,16,12,"Loader\nshuffle,\nbatch",B); box(46,40,16,12,"Model\nforward",T); box(68,40,14,12,"Loss",O); box(87,40,11,12,"Metric",P)
box(68,14,14,12,"Backward\ngradients",O); box(46,14,16,12,"Clip,\noptimizer\nstep",T); box(24,14,16,12,"Weights\nupdated",T)
for a,b in [(18,24),(40,46),(62,68),(82,87)]: arr(a,46,b,46)
arr(75,40,75,26); arr(68,20,62,20); arr(46,20,40,20); arr(32,26,52,40,"#357a70")
bug(4,54,1); bug(26,54,2); bug(48,54,3); bug(70,54,4); bug(89,54,5); bug(77,28,6); bug(48,28,7); bug(26,28,8)
txt=["1 labels wrong, leakage, bad scaling","2 inputs and labels misaligned","3 shape or init error, eval vs train mode","4 wrong loss, logits vs probabilities, log(0)","5 metric hides the problem (imbalance)","6 vanishing, exploding, nan gradients","7 no zero_grad, no clip, wrong lr","8 frozen or missing parameters"]
for i,t in enumerate(txt): ax.text(2+(i//4)*50,8-(i%4)*2.3,t,fontsize=8.6,color="#222")
ax.set_title("One training step as a data flow, with the eight places it breaks",fontsize=12)
fig.tight_layout(); fig.savefig("ch04d_pipeline.png",dpi=110)
