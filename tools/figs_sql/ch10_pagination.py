import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, sqlite3, random
random.seed(7)
db=sqlite3.connect(":memory:",isolation_level=None)
db.execute("CREATE TABLE big (id INTEGER PRIMARY KEY, created TEXT)")
db.executemany("INSERT INTO big VALUES (?,?)",[(i,"2024-%02d-%02d"%(random.randint(1,12),random.randint(1,28))) for i in range(1,50001)])
db.execute("CREATE INDEX i_ci ON big(created,id)")
def steps(q,a=()):
    n=[0]
    def h(): n[0]+=1; return 0
    db.set_progress_handler(h,1); db.execute(q,a).fetchall(); db.set_progress_handler(None,0); return n[0]
pages=[1,50,100,200,300,400,500]; o=[];k=[]
for p in pages:
    off=(p-1)*20
    o.append(steps("SELECT id,created FROM big ORDER BY created,id LIMIT 20 OFFSET ?",(off,)))
    last=db.execute("SELECT created,id FROM big ORDER BY created,id LIMIT 1 OFFSET ?",(max(off-1,0),)).fetchone()
    k.append(steps("SELECT id,created FROM big WHERE (created,id)>(?,?) ORDER BY created,id LIMIT 20",last))
fig,ax=plt.subplots(figsize=(8,4.2))
ax.plot(pages,o,"-o",color="#b84a22",lw=2,label="OFFSET paging")
ax.plot(pages,k,"-s",color="#2b4fd6",lw=2,label="keyset paging")
ax.set_xlabel("page number (20 rows per page)"); ax.set_ylabel("SQLite VM steps")
ax.set_title("Cost of fetching one page from a 50,000-row table"); ax.legend(); ax.grid(alpha=.3)
for sp in("top","right"): ax.spines[sp].set_visible(False)
plt.tight_layout(); plt.savefig("ch10_pagination.png",dpi=110); print(list(zip(pages,o,k)))
