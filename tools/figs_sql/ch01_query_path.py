import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig,ax=plt.subplots(figsize=(8,4.2)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,6)
def box(x,y,w,h,t,c,sub=None):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05",fc="white",ec=c,lw=2))
    ax.text(x+w/2,y+h/2+(0.15 if sub else 0),t,ha="center",va="center",fontsize=10.5,color=c,weight="bold")
    if sub: ax.text(x+w/2,y+h/2-0.28,sub,ha="center",va="center",fontsize=8,color="#333")
def arr(x1,y1,x2,y2,c="#444"):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=14,color=c,lw=1.6))
box(0.2,4.3,2.2,1.2,"Your query",B,"SELECT ... FROM ...")
box(3.0,4.3,2.0,1.2,"Parser",O,"is the text valid SQL?")
box(5.6,4.3,2.1,1.2,"Planner",T,"pick the cheapest plan")
box(8.2,4.3,1.6,1.2,"Executor",P,"runs the plan")
arr(2.45,4.9,2.95,4.9); arr(5.05,4.9,5.55,4.9); arr(7.75,4.9,8.15,4.9)
box(3.0,1.9,4.7,1.2,"Storage engine",B,"cache, pages, indexes, write-ahead log")
arr(9.0,4.25,7.0,3.15)
box(3.0,0.1,4.7,1.0,"Files on disk",R,"table pages + log file")
arr(5.35,1.85,5.35,1.15)
arr(5.0,3.15,1.3,4.25,T)
ax.text(1.0,3.0,"result rows\ncome back",fontsize=9,color=T,ha="center")
ax.text(4.0,3.75,"syntax error?\nstops here",fontsize=8,color=O,ha="center")
ax.text(6.65,3.75,"you only said WHAT;\nthis picks HOW",fontsize=8,color=T,ha="center")
ax.set_title("A SQL query on its way through a database engine",fontsize=11)
plt.tight_layout(); plt.savefig("ch01d_query_path.png",dpi=110)
