import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,R,V="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
import sqlite3,sys
sys.path.insert(0,".")
from _kit import shop
db=shop()
rows=db.execute("select p.name, qty*unit_price from order_items oi join products p using(product_id) order by p.product_id, oi.order_id").fetchall()
names=["Keyboard","Mouse","Notebook","Pen Pack","Desk Lamp"]
cols=[B,O,T,V,R]
fig,(a,b)=plt.subplots(1,2,figsize=(8,4.2),gridspec_kw={"width_ratios":[1.5,1]})
a.set_title("20 order lines sorted into 5 piles (one block = one line)",fontsize=9.5)
for i,n in enumerate(names):
    vals=[v for nm,v in rows if nm==n]; bottom=0
    for v in vals:
        a.bar(i,1,bottom=bottom,color=cols[i],edgecolor="white",lw=1.5,width=.7)
        a.text(i,bottom+.5,str(v),ha="center",va="center",color="white",fontsize=7.5)
        bottom+=1
    a.text(i,bottom+.2,f"{len(vals)} lines",ha="center",fontsize=8)
a.set_xticks(range(5)); a.set_xticklabels(names,fontsize=8); a.set_ylim(0,8); a.set_yticks([])
for s in("top","right","left"): a.spines[s].set_visible(False)
tot=[sum(v for nm,v in rows if nm==n) for n in names]
b.barh(names[::-1],tot[::-1],color=cols[::-1])
for i,t in enumerate(tot[::-1]): b.text(t+80,i,str(t),va="center",fontsize=9)
b.set_xlim(0,7500); b.set_title("SUM per pile = 14560 in all",fontsize=9.5)
b.tick_params(labelsize=8)
for s in("top","right"): b.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("ch03d_piles.png",dpi=110)
