import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B,O,T,R,V="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig,ax=plt.subplots(figsize=(8,4.2)); ax.axis("off"); ax.set_xlim(0,100); ax.set_ylim(0,56)
def box(x,y,w,h,t,c,fs=8):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.3",fc="white",ec=c,lw=1.8)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs)
def arr(x1,y1,x2,y2,t=""):
    ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="->",color="#555"))
    if t: ax.text((x1+x2)/2+1,(y1+y2)/2+1,t,fontsize=7.5,color="#555")
ax.set_title("Decision flow: from the question to the query",fontsize=11)
box(1,44,26,9,"1. Say the grain:\n'one row per ___'",B)
box(36,44,26,9,"2. Which table holds that\ngrain? Which joins add rows?",B)
box(71,44,27,9,"3. Row conditions?\nput them in WHERE",O)
arr(27,48.5,36,48.5); arr(62,48.5,71,48.5)
box(1,26,26,9,"4. GROUP BY the grain key\n(or none: one-row KPI)",T)
box(36,26,26,9,"5. Aggregate: COUNT, SUM,\nAVG; FILTER for conditions",T)
box(71,26,27,9,"6. Condition on an aggregate?\nput it in HAVING",R)
arr(85,44,14,35.2); arr(27,30.5,36,30.5); arr(62,30.5,71,30.5)
box(1,8,26,9,"7. Order, LIMIT,\nround, NULLIF",V)
box(36,8,26,9,"8. Check: groups add up\nto the plain total?",V)
box(71,8,27,9,"Fails? Count rows after each\njoin; test on 1 group by hand",R)
arr(85,26,14,17.2); arr(27,12.5,36,12.5); arr(62,12.5,71,12.5,"no")
plt.tight_layout(); plt.savefig("ch03d_flow.png",dpi=110)
