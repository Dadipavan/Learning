import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13})

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.axis("off");ax.set_xlim(0,16);ax.set_ylim(-0.2,5.2)
def box(x,y,t,c="#eef",tc="black"):
    ax.text(x,y,t,ha="center",va="center",fontsize=12,color=tc,bbox=dict(boxstyle="round",fc=c,ec="black"))
def edge(x1,y1,x2,y2,l,c=T,dash=False):
    ax.plot([x1,x2],[y1-0.25,y2+0.25],color=c,ls="--" if dash else "-",lw=1.6)
    ax.text((x1+x2)/2+0.4,(y1+y2)/2,l,fontsize=11,color=c)
box(8,4.7,"[]")
box(3,3.2,"[1]");edge(8,4.7,3,3.2,"1")
box(8,3.2,"[2] (first 2)");edge(8,4.7,8,3.2,"2")
box(13.3,3.2,"[2] (second 2)",R,"white");edge(8,4.7,13.3,3.2,"2 again: skip",R,True)
box(1.5,1.7,"[1,2]");edge(3,3.2,1.5,1.7,"2")
box(5.2,1.7,"[1,2] again",R,"white");edge(3,3.2,5.2,1.7,"skip",R,True)
box(1.5,0.3,"[1,2,2]");edge(1.5,1.7,1.5,0.3,"2")
box(8,1.7,"[2,2]");edge(8,3.2,8,1.7,"2")
ax.text(13.3,1.4,"red = same value as the\nprevious sibling:\nnever started twice",ha="center",fontsize=11.5,color=R)
ax.text(0.2,5.0,"subsets of [1,2,2], sorted",fontsize=12,weight="bold")
fig.tight_layout();fig.savefig("dsa6_dups.png")
