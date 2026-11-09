import sqlite3
from common import *
db = sqlite3.connect(":memory:")
db.executescript("create table author(id integer primary key, name text); create table book(id integer primary key, author_id int, title text);")
for a in range(1, 51):
    db.execute("insert into author values (?,?)", (a, f"a{a}"))
    for b in range(3):
        db.execute("insert into book(author_id,title) values (?,?)", (a, f"t{a}{b}"))
counts = []
for n in (5, 10, 25, 50):
    q = [0]
    db.set_trace_callback(lambda s: q.__setitem__(0, q[0] + 1))
    for (aid,) in db.execute("select id from author limit ?", (n,)).fetchall():
        db.execute("select title from book where author_id=?", (aid,)).fetchall()
    naive = q[0]; q[0] = 0
    db.execute("select a.id, b.title from author a join book b on b.author_id=a.id where a.id<=?", (n,)).fetchall()
    counts.append((n, naive, q[0]))
fig, ax = plt.subplots(figsize=(8, 4.2))
xs = [c[0] for c in counts]
ax.plot(xs, [c[1] for c in counts], "o-", color=RED, lw=2, label="N+1 loop (1 + N queries)")
ax.plot(xs, [c[2] for c in counts], "s-", color=TEAL, lw=2, label="one JOIN (1 query)")
ax.set_xlabel("number of authors N"); ax.set_ylabel("SQL statements sent"); ax.grid(alpha=0.3); ax.legend()
ax.set_title("Query count: N+1 grows with the data, a join does not")
save(fig, "ch12_nplus1.png")
print(counts)
