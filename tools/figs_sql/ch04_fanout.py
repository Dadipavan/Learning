import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
B,O,T,G="#2b4fd6","#b84a22","#357a70","#999999"
fig,(a,b)=plt.subplots(1,2,figsize=(8,4.2),gridspec_kw={"width_ratios":[1.25,1]})
cust=[("Asha",[101,103,106,111]),("Ravi",[102,108,114]),("Sana",[])]
a.axis("off"); a.set_xlim(0,10); a.set_ylim(-.5,8.5)
a.set_title("LEFT JOIN: each customer meets its orders",fontsize=10)
orders=[101,103,106,111,102,108,114]
oy={o:7.4-i*1.0 for i,o in enumerate(orders)}
cy={"Asha":5.4,"Ravi":2.4,"Sana":0.2}
for n,y in cy.items():
    a.text(1.2,y,n,ha="center",va="center",fontsize=10,color=B if n!="Sana" else O,bbox=dict(boxstyle="round",fc="white",ec=B if n!="Sana" else O))
for o,y in oy.items(): a.text(8.2,y,str(o),ha="center",va="center",fontsize=9,bbox=dict(boxstyle="round",fc="white",ec=T))
for n,os in cust:
    for o in os: a.plot([1.9,7.7],[cy[n],oy[o]],color=B,lw=1.2)
a.text(5,.2,"no match: one row with NULL order",ha="center",va="center",fontsize=8.5,color=O)
labels=["customers","+ orders","+ order_items"]; vals=[8,16,22]
b.bar(labels,vals,color=[B,O,O])
for i,v in enumerate(vals): b.text(i,v+.4,str(v),ha="center",fontsize=11)
b.set_ylabel("rows in the result"); b.set_title("Row count after each LEFT JOIN",fontsize=10)
b.tick_params(axis="x",labelsize=8.5)
for sp in("top","right"): b.spines[sp].set_visible(False)
plt.tight_layout(); plt.savefig("ch04_fanout.png",dpi=110)
