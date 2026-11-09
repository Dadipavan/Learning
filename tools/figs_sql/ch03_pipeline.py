import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B,O,T,R,V="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig,ax=plt.subplots(figsize=(8,4.2)); ax.axis("off"); ax.set_xlim(0,100); ax.set_ylim(0,52)
ax.set_title("Logical order of a grouped query (rows left after each step)",fontsize=11)
steps=[("FROM + JOIN","orders x order_items","20 rows",B),("WHERE","status = 'paid'","18 rows",O),
("GROUP BY","customer_id","5 groups",T),("HAVING","SUM(...) > 1500","3 groups",R),("SELECT","customer_id, SUM(...)","3 rows",V),("ORDER BY","spent DESC","3 rows",B)]
w=14.2;gap=2.5
for i,(a,b,c,col) in enumerate(steps):
    x=1+i*(w+gap)*0.98
    ax.add_patch(FancyBboxPatch((x,20),w,18,boxstyle="round,pad=0.3",fc="white",ec=col,lw=2))
    ax.text(x+w/2,34,a,ha="center",fontsize=8.5,fontweight="bold",color=col)
    ax.text(x+w/2,28.5,b,ha="center",fontsize=6.8,wrap=True)
    ax.text(x+w/2,23,c,ha="center",fontsize=9,color=col,fontweight="bold")
    ax.text(x+w/2,41,str(i+1),ha="center",fontsize=11,color="#555")
    if i<5: ax.annotate("",xy=(x+w+gap*0.95,29),xytext=(x+w+0.4,29),arrowprops=dict(arrowstyle="->",color="#555"))
ax.text(50,12,"WHERE cannot see SUM(...): the groups do not exist yet at step 2.",ha="center",fontsize=9.5,color=O)
ax.text(50,6,"HAVING can: it runs at step 4, after the groups are built.  An alias made in SELECT (step 5) is born too late for WHERE.",ha="center",fontsize=8.5,color="#333")
plt.tight_layout(); plt.savefig("ch03d_pipeline.png",dpi=110)
