import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig,ax=plt.subplots(figsize=(8,4.2)); ax.set_xlim(0,100); ax.set_ylim(0,60); ax.axis("off")
def box(x,y,w,h,t,c,fs=8.6):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.3,rounding_size=1.2",fc="white",ec=c,lw=2)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs)
def ar(x1,y1,x2,y2,t=None):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",lw=1.6,color="#444"))
    if t: ax.text((x1+x2)/2+0.6,(y1+y2)/2+1,t,fontsize=8,color=R)
box(1,45,20,11,"Loss is nan or inf?",R); box(1,28,20,11,"First loss far\nfrom ln K?",O); box(1,11,20,11,"Overfit 16\nexamples fails?",O)
box(30,45,30,11,"Pattern 2: numerics\nlog(0), exp overflow, lr, bad data",R)
box(30,28,30,11,"Pattern 1: init or labels\nlast layer scale, label range",O)
box(30,11,30,11,"Pattern 6: code bug\nzero_grad, optimizer params, update",O)
box(70,45,29,11,"Loss spikes or jumps?\nPattern 3: clip, lower lr, warmup",B)
box(70,28,29,11,"Train good, val bad?\nPattern 4: regularize, data",T)
box(70,11,29,11,"Both bad and flat?\nPattern 5: capacity, lr, features",P)
ar(21,50.5,30,50.5,"yes"); ar(21,33.5,30,33.5,"yes"); ar(21,16.5,30,16.5,"yes")
ar(11,45,11,39,"no"); ar(11,28,11,22,"no")
ax.text(84.5,58.5,"Checks pass? Read the curves:",fontsize=9,ha="center",color="#222")
ax.text(3,2.5,"If all three checks pass, the code is probably fine: use the right column to read the curves.",fontsize=8.6,color="#222")
ax.set_title("Decision flow: ask the cheapest question first",fontsize=12)
fig.tight_layout(); fig.savefig("ch04d_flow.png",dpi=110)
