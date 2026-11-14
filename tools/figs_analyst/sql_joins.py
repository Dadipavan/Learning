import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _sqldata import make
con = make()
n = lambda s: con.execute(s).fetchone()[0]
vals = [
 ("INNER JOIN", n("SELECT COUNT(*) FROM customers c JOIN orders o ON o.cust_id=c.cust_id"), "#2b4fd6"),
 ("LEFT JOIN\n(customers first)", n("SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON o.cust_id=c.cust_id"), "#357a70"),
 ("LEFT JOIN +\nIS NULL (anti)", n("SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON o.cust_id=c.cust_id WHERE o.order_id IS NULL"), "#b84a22"),
 ("LEFT JOIN, status\nin WHERE", n("SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON o.cust_id=c.cust_id WHERE o.status='delivered'"), "#aa2d26"),
 ("LEFT JOIN, status\nin ON", n("SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON o.cust_id=c.cust_id AND o.status='delivered'"), "#6a2fd0"),
]
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
bars = ax.bar([v[0] for v in vals], [v[1] for v in vals], color=[v[2] for v in vals])
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v[1] + 0.3, str(v[1]), ha="center", fontsize=12, fontweight="bold")
ax.set_ylabel("rows returned", fontsize=12)
ax.set_title("Same two tables (6 customers, 14 orders), five different row counts", fontsize=12)
ax.tick_params(axis="x", labelsize=9); ax.tick_params(axis="y", labelsize=11)
ax.set_ylim(0, 18)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig("sql_joins.png")
