import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
B,O,T,R,P="#2b4fd6","#b84a22","#357a70","#aa2d26","#6a2fd0"
fig,ax=plt.subplots(figsize=(8,4.2)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,6.4)
def table(x,y,name,cols,c,w=2.7):
    h=0.45*(len(cols)+1)
    ax.add_patch(FancyBboxPatch((x,y-h),w,h,boxstyle="square,pad=0",fc="white",ec=c,lw=2))
    ax.add_patch(FancyBboxPatch((x,y-0.45),w,0.45,boxstyle="square,pad=0",fc=c,ec=c))
    ax.text(x+w/2,y-0.22,name,ha="center",va="center",color="white",weight="bold",fontsize=10)
    for i,(t,k) in enumerate(cols):
        yy=y-0.45*(i+1)-0.22
        ax.text(x+0.1,yy,t,va="center",fontsize=8.5)
        if k: ax.text(x+w-0.1,yy,k,va="center",ha="right",fontsize=8,color=R if k=="PK" else P,weight="bold")
    return x,y,w,h
table(0.2,5.8,"customers",[("customer_id","PK"),("name",""),("city",""),("signup_date",""),("referrer_id","FK")],B)
table(3.9,5.8,"orders",[("order_id","PK"),("customer_id","FK"),("order_date",""),("status",""),("coupon","")],O)
table(7.6,5.8,"order_items",[("order_id","PK,FK"),("product_id","PK,FK"),("qty",""),("unit_price","")],T)
table(7.6,2.6,"products",[("product_id","PK"),("name",""),("category",""),("price","")],P)
def line(x1,y1,x2,y2,l1,l2,c="#333"):
    ax.plot([x1,x2],[y1,y2],color=c,lw=1.6)
    ax.text(x1+(0.1 if x2>x1 else -0.1),y1+0.15,l1,fontsize=10,weight="bold",color=c,ha="left" if x2>x1 else "right")
    ax.text(x2+(-0.1 if x2>x1 else 0.1),y2+0.15,l2,fontsize=10,weight="bold",color=c,ha="right" if x2>x1 else "left")
line(2.9,4.8,3.9,4.8,"1","N")
line(6.6,4.8,7.6,4.8,"1","N")
ax.plot([8.95,8.95],[3.6,2.6],color="#333",lw=1.6)
ax.text(9.05,3.2,"N",fontsize=10,weight="bold"); ax.text(9.05,2.75,"1",fontsize=10,weight="bold")
ax.text(1.55,2.2,"customers.referrer_id points back\nto customers.customer_id\n(self-reference, can be NULL)",fontsize=8.5,color=P,ha="center")
ax.text(0.2,0.7,"1 = exactly one parent row    N = many child rows\norder_items is the bridge: orders and products are many-to-many",fontsize=9,color="#333")
ax.set_title("The shop database used from Chapter 2",fontsize=11)
plt.tight_layout(); plt.savefig("ch01d_er_shop.png",dpi=110)
