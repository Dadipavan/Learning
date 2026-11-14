import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, sqlite3, time, random
B,O,T,R="#2b4fd6","#b84a22","#357a70","#aa2d26"
random.seed(1)
con=sqlite3.connect(":memory:")
con.execute("CREATE TABLE ev(id INTEGER PRIMARY KEY, user_id INTEGER, note TEXT)")
N=1_000_000
con.executemany("INSERT INTO ev VALUES(?,?,?)",((i,random.randrange(N),"x"*20) for i in range(N)))
def t(sql,args,reps=20):
    s=time.perf_counter()
    for _ in range(reps): con.execute(sql,args).fetchall()
    return (time.perf_counter()-s)/reps*1000
a=t("SELECT * FROM ev WHERE user_id=?",(777,),3)
b=t("SELECT * FROM ev WHERE id=?",(777,),200)
con.execute("CREATE INDEX ix ON ev(user_id)")
c=t("SELECT * FROM ev WHERE user_id=?",(777,),200)
print(a,b,c)
fig,(x1,x2)=plt.subplots(1,2,figsize=(8,4.2))
labs=["no index\n(full scan)","primary key\nlookup","index on\nuser_id"]
vals=[a,b,c]
x1.bar(labs,vals,color=[O,B,T]); x1.set_yscale("log"); x1.set_ylabel("ms per query (log scale)")
for i,v in enumerate(vals): x1.text(i,v*1.3,f"{v:.3f}" if v<1 else f"{v:.0f}",ha="center",fontsize=10)
x1.set_title("1,000,000 rows, find one user",fontsize=10); x1.tick_params(axis="x",labelsize=8.5)
x1.set_ylim(min(vals)/3,max(vals)*6)
rows=[1_000_000,~0 and 1,1]
x2.bar(["full scan","primary key","index"],[1_000_000,1,1],color=[O,B,T]); x2.set_yscale("log")
x2.set_ylabel("rows the engine looks at (about)"); x2.set_title("Rows examined",fontsize=10)
for i,v in enumerate([1_000_000,1,1]): x2.text(i,v*1.4,f"{v:,}",ha="center",fontsize=10)
x2.set_ylim(0.5,1e8); x2.tick_params(axis="x",labelsize=8.5)
for a_ in (x1,x2):
    for sp in("top","right"): a_.spines[sp].set_visible(False)
plt.tight_layout(); plt.savefig("ch01d_scan_vs_index.png",dpi=110)
