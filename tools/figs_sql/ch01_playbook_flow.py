import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig,ax=plt.subplots(figsize=(8,4.2)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(-0.3,6.4)
def box(x,y,w,h,t,c,fs=8.5):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05",fc="white",ec=c,lw=1.8))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,color="#111")
def arr(a,b,c="#444"):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=12,color=c,lw=1.4))
box(4.2,5.2,3.6,1.0,"Read the problem.\nWhat is the thing being asked?",B)
box(0.1,3.2,2.6,1.2,"Given a table or\nCSV: what is one row?\n(grain, key)",T)
box(3.1,3.2,2.6,1.2,"Two things related:\nhow many on each side?\n(cardinality, FK side)",O)
box(6.1,3.2,2.6,1.2,"A rule must hold:\nconstraint or type?\n(NOT NULL, CHECK, ...)",P)
box(9.1,3.2,2.8,1.2,"Unknown database:\nlook before you write\n(introspect)",R)
for x in (1.4,4.4,7.4,10.5): arr((6,5.15),(x,4.45))
box(0.1,1.2,2.6,1.1,"Pattern 1, 3, 7:\nkey, split, fix design",T)
box(3.1,1.2,2.6,1.1,"Pattern 2, 8:\nFK side, bridge,\nrow count of a join",O)
box(6.1,1.2,2.6,1.1,"Pattern 4, 5:\ntypes, constraints,\npredict insert result",P)
box(9.1,1.2,2.8,1.1,"Pattern 6:\nschema, counts,\norphans, NULL rates",R)
for x in (1.4,4.4,7.4,10.5): arr((x,3.15),(x,2.35))
box(2.5,0.0,7.0,0.75,"Check: run it on a tiny sample, compare with your hand answer",B,9)
for x in (1.4,4.4,7.4,10.5): arr((x,1.15),(6 if x<6 else 6,0.8),"#999")
ax.set_title("Decision flow for relational model problems",fontsize=11)
plt.tight_layout(); plt.savefig("ch01d_playbook_flow.png",dpi=110)
