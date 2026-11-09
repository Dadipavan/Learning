import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
plt.rcParams.update({"font.size":13})

fig,ax=plt.subplots(figsize=(8,4.2),dpi=110)
ax.axis("off");ax.set_xlim(0,16);ax.set_ylim(-0.3,5.0)
def box(x,y,t,c="#eef",tc="black",fs=12):
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,color=tc,bbox=dict(boxstyle="round",fc=c,ec="black"))
box(9,4.5,"''")
ax.text(0.1,3.1,"digit 2 -> a b c",fontsize=12,color=B,weight="bold")
ax.text(0.1,2.5,"digit 3 -> d e f",fontsize=12,color=O,weight="bold")
for k,(ch,x) in enumerate(zip("abc",[4.5,9,13.5])):
    ax.plot([9,x],[4.25,3.35],color="#888");box(x,3.1,ch)
    for j,c2 in enumerate("def"):
        xx=x+(j-1)*1.4
        ax.plot([x,xx],[2.85,1.85],color="#888")
        box(xx,1.6,ch+c2,T,"white",11)
ax.text(8.5,0.4,"3 x 3 = 9 leaves: ad ae af bd be bf cd ce cf",ha="center",fontsize=13,weight="bold",color=R)
fig.tight_layout();fig.savefig("dsa6_letters.png")
