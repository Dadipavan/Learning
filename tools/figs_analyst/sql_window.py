import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _sqldata import make
con = make()
rows = con.execute("""SELECT order_id, amount,
 SUM(amount) OVER (ORDER BY order_date, order_id) AS running,
 AVG(amount) OVER (ORDER BY order_date, order_id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS ma3
 FROM orders WHERE status='delivered' ORDER BY order_date, order_id""").fetchall()
k = list(range(1, len(rows) + 1))
fig, (a, b) = plt.subplots(1, 2, figsize=(8, 4.2), dpi=110)
a.step(k, [r[2] for r in rows], where="post", color="#2b4fd6", lw=2)
a.plot(k, [r[2] for r in rows], "o", color="#2b4fd6")
a.set_title("SUM(amount) OVER (ORDER BY date)\nrunning total", fontsize=11)
a.set_xlabel("delivered order, in date order", fontsize=11); a.set_ylabel("Rs", fontsize=11)
b.bar(k, [r[1] for r in rows], color="#b9c4ef", label="order amount")
b.plot(k, [r[3] for r in rows], "-o", color="#b84a22", lw=2, label="3-order moving average")
b.set_title("AVG(amount) OVER (... ROWS BETWEEN\n2 PRECEDING AND CURRENT ROW)", fontsize=11)
b.set_xlabel("delivered order, in date order", fontsize=11); b.legend(fontsize=9, frameon=False)
for ax in (a, b):
    ax.tick_params(labelsize=10)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("sql_window.png")
