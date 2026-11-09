import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig,axs=plt.subplots(1,3,figsize=(8,4.2))
def dots(ax,xs,ys,labs,c):
    for x,y,l in zip(xs,ys,labs):
        ax.scatter([x],[y],s=1100,color="white",edgecolor=c,lw=2,zorder=3); ax.text(x,y,l,ha="center",va="center",fontsize=7,zorder=4)
for ax in axs: ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,6)
a=axs[0]; a.set_title("One-to-many\nFK on the many side",fontsize=9)
dots(a,[1.5]*2,[4.5,1.5],["10","20"],B); dots(a,[8.3]*3,[5,3,1],["Asha","Meena","Ravi"],O)
for y1,y2 in((4.5,5),(4.5,3),(1.5,1)): a.plot([1.9,8.0],[y1,y2],color="#555",lw=1.3,zorder=1)
a.text(1.5,0.1,"department",ha="center",fontsize=8.5,color=B); a.text(8.5,0.1,"employee (has dept_id)",ha="center",fontsize=8,color=O)
b=axs[1]; b.set_title("Many-to-many\nneeds a bridge table",fontsize=9)
dots(b,[1.2]*2,[4.5,1.5],["Asha","Ravi"],B); dots(b,[8.8]*2,[4.5,1.5],["SQL","Py"],T)
for y in (4.5,3.0,1.5): b.add_patch(plt.Rectangle((4,y-.45),2,.9,fc="white",ec=O,lw=1.8))
for y,t in((4.5,"A,SQL"),(3.0,"R,SQL"),(1.5,"R,Py")): b.text(5,y,t,ha="center",va="center",fontsize=8)
for (x1,y1,x2,y2) in((1.8,4.5,4,4.5),(1.8,4.5,4,3.1),(1.8,1.5,4,3.0),(1.8,1.5,4,1.5)): b.plot([x1,x2],[y1,y2],color="#555",lw=1.1)
for (x1,y1,x2,y2) in((6,4.5,8.3,4.5),(6,3.0,8.3,4.4),(6,1.5,8.3,1.5)): b.plot([x1,x2],[y1,y2],color="#555",lw=1.1)
b.text(5,0.3,"employee_skills (bridge)",ha="center",fontsize=8.5,color=O)
c=axs[2]; c.set_title("One-to-one\nrare, FK also UNIQUE",fontsize=9)
dots(c,[1.5]*3,[5,3,1],["u1","u2","u3"],B); dots(c,[8.5]*3,[5,3,1],["p1","p2","p3"],T)
for y in (5,3,1): c.plot([1.9,8.1],[y,y],color="#555",lw=1.3,zorder=1)
c.text(1.5,0.1,"user",ha="center",fontsize=8.5,color=B); c.text(8.5,0.1,"profile",ha="center",fontsize=8.5,color=T)
plt.subplots_adjust(top=0.82,bottom=0.05,left=0.02,right=0.98); plt.savefig("ch01d_cardinality.png",dpi=110)
