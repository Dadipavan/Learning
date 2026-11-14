import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

import sqlite3, time, tempfile, os
rows = [(i, f"name{i}", i * 0.5) for i in range(5000)]
def run(mode):
    d = tempfile.mkdtemp(); con = sqlite3.connect(os.path.join(d, "t.db"))
    con.execute("create table t(id integer, name text, v real)")
    t0 = time.perf_counter()
    if mode == "commit each row":
        for r in rows:
            con.execute("insert into t values (?,?,?)", r); con.commit()
    elif mode == "one transaction":
        with con:
            for r in rows:
                con.execute("insert into t values (?,?,?)", r)
    else:
        with con:
            con.executemany("insert into t values (?,?,?)", rows)
    dt = time.perf_counter() - t0; con.close(); return dt * 1000
modes = ["commit each row", "one transaction", "executemany"]
vals = [run(m) for m in modes]
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
bars = ax.bar(modes, vals, color=[R, O, T])
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.0f} ms", ha="center", va="bottom")
ax.set_yscale("log"); ax.set_ylim(0.5, 20000)
ax.set_ylabel("time to insert 5,000 rows (ms, log scale)")
ax.set_title("Transactions decide SQLite write speed (measured, varies)")
fig.tight_layout(); fig.savefig("lib20_sqlite_insert.png")
