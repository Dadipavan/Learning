from _kit import *
db=shop()
base="""CREATE VIEW paid_lines AS
SELECT p.category, substr(o.order_date, 1, 7) AS month, i.qty * i.unit_price AS amt
FROM orders o JOIN order_items i ON i.order_id = o.order_id JOIN products p ON p.product_id = i.product_id
WHERE o.status = 'paid';"""
db.executescript(base)
r1="""SELECT category, month, revenue FROM (
  SELECT category, month, sum(amt) AS revenue FROM paid_lines GROUP BY category, month
  UNION ALL
  SELECT category, 'ALL', sum(amt) FROM paid_lines GROUP BY category
  UNION ALL
  SELECT 'ALL', 'ALL', sum(amt) FROM paid_lines
)
ORDER BY (category = 'ALL'), category, (month = 'ALL'), month;"""
o1=run(db,r1)
chk=run(db,"""SELECT sum(amt) AS detail_total, (SELECT sum(amt) FROM paid_lines) AS grand FROM paid_lines GROUP BY () """) if False else ""
import sqlite3
# dynamic pivot
dyn='''import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE sales (category TEXT, month TEXT, amt INTEGER);
INSERT INTO sales VALUES ('Electronics','2024-01',2100),('Electronics','2024-02',1500),
 ('Stationery','2024-01',160),('Stationery','2024-02',120),('Home','2024-02',900);
""")
months = [r[0] for r in db.execute("SELECT DISTINCT month FROM sales ORDER BY month")]
cols = ",\\n  ".join("sum(CASE WHEN month = '%s' THEN amt ELSE 0 END) AS \\"m%s\\"" % (m, m.replace("-", "_")) for m in months)
sql = "SELECT category,\\n  " + cols + "\\nFROM sales GROUP BY category ORDER BY category"
print(sql)
print()
cur = db.execute(sql)
print([d[0] for d in cur.description])
for row in cur: print(row)
db.execute("INSERT INTO sales VALUES ('Home','2024-03',250)")
months = [r[0] for r in db.execute("SELECT DISTINCT month FROM sales ORDER BY month")]
print("after a new month arrives, columns would be:", months)
'''
dynout=pyrun(dyn)
unp=exec_sql(db,"""CREATE TABLE targets (category TEXT, q1 INTEGER, q2 INTEGER, q3 INTEGER);
INSERT INTO targets VALUES ('Electronics', 5000, 5500, 6000), ('Home', 2000, 2100, 2300);
SELECT category, 'q1' AS quarter, q1 AS target FROM targets
UNION ALL SELECT category, 'q2', q2 FROM targets
UNION ALL SELECT category, 'q3', q3 FROM targets
ORDER BY category, quarter;""")
js=exec_sql(db,"""SELECT t.category, j.key AS quarter, j.value AS target
FROM targets t, json_each(json_object('q1', t.q1, 'q2', t.q2, 'q3', t.q3)) AS j
ORDER BY t.category, j.key;""")
body=f'''
<h2 id="x7-4-reporting-lab-rollup-pivot-and-unpivot-you-can-run-anywhere">7.4 Reporting Lab: ROLLUP, Pivot and Unpivot You Can Run Anywhere</h2>
{co("blue","INTUITION","A finance report has detail lines, a subtotal under each group and a grand total at the bottom. <code>ROLLUP</code> is the keyword that produces all of those in one query. SQLite does not have it, but a report is only a stack of group-by queries at different levels, so <code>UNION ALL</code> builds the same thing. Doing it by hand once shows exactly what <code>ROLLUP</code> and <code>GROUPING()</code> do for you.")}
{P("7.4.1","Build a revenue report by category and month with a subtotal per category and a grand total, using only portable SQL. First a view of paid lines, then three group-by levels. Predict first: 3 categories x months with sales, plus one subtotal row per category, plus one grand-total row.")}
{sql(base)}
{sql(r1)}
{text(o1)}
{steps([("Step 1","Level 0 groups by both columns: the detail rows. Level 1 groups by category only and writes the text <code>ALL</code> in the month column. Level 2 has no group at all, one grand-total row."),("Step 2","All three branches have the same column list and types, so <code>UNION ALL</code> is legal. Use <code>UNION ALL</code>, not <code>UNION</code>, so identical totals are not merged."),("Step 3","The three queries sit inside one outer <code>SELECT</code> because an <code>ORDER BY</code> on a <code>UNION</code> may only name result columns. The outer <code>ORDER BY</code> puts the <code>ALL</code> rows after the details by sorting on the boolean tests <code>(month = 'ALL')</code>, which are 0 or 1."),("Check","Each category subtotal equals the sum of its detail rows, and the grand total equals the sum of the three subtotals."),("PostgreSQL form","<code>GROUP BY ROLLUP (category, month)</code> gives the same rows, with <code>NULL</code> instead of <code>ALL</code>, in one pass over the data (not run here). Use <code>GROUPING(month)</code>, which is 1 when the <code>NULL</code> is a subtotal marker and 0 when the data itself was <code>NULL</code>, to label them.")])}
{co("red","COMMON MISTAKE","Using <code>COALESCE(month, 'ALL')</code> to label subtotal rows in a <code>ROLLUP</code> query. If the data has a real <code>NULL</code> month, it is also relabelled <code>ALL</code> and you cannot tell a data gap from a subtotal. Use <code>CASE WHEN GROUPING(month) = 1 THEN 'ALL' ELSE month END</code>. The same holds for the hand-made version here: if <code>month</code> could be NULL, the detail branch must handle it first.")}
{tbl(["Operator","Levels produced for (a, b)","Rows if a has 3 values and b has 4 (all combinations present)"],[["<code>GROUP BY a, b</code>","(a,b)","12"],["<code>ROLLUP (a, b)</code>","(a,b), (a), ()","12 + 3 + 1 = 16"],["<code>CUBE (a, b)</code>","(a,b), (a), (b), ()","12 + 3 + 4 + 1 = 20"],["<code>GROUPING SETS ((a),(b))</code>","exactly the sets you list","3 + 4 = 7"]])}
<p>Rule of thumb: <code>ROLLUP</code> is for hierarchies (country, state, city), where the order of columns matters. <code>CUBE</code> is for independent dimensions where you want every cross-total. <code>GROUPING SETS</code> is for when you know exactly which levels the report needs, and it is the cheapest.</p>
<h3>Dynamic pivot: the column list comes from the data</h3>
<p>Plain SQL cannot create columns whose names depend on data, but your program can write the SQL. Query the distinct values, build one <code>SUM(CASE ...)</code> per value, then run the generated text. This is the standard answer to the interview question "pivot when I do not know the months in advance".</p>
{P("7.4.2","Generate a pivot of sales by category with one column per month found in the data. Predict first: two month columns now, and three after a March row arrives.")}
{py(dyn)}
{text(dynout)}
{steps([("Step 1","The first query asks the data which months exist."),("Step 2","A string join builds one aggregate column per month. Column aliases are quoted and cleaned (<code>-</code> becomes <code>_</code>), since a name like <code>2024-01</code> is not a legal bare identifier."),("Step 3","The generated SQL is ordinary SQL, so you can print and inspect it. Electronics has 2100 in January and 1500 in February, as the data says."),("Step 4","When March data appears, the list of months grows to three and the next run of the generator produces three columns. Nobody edits the query.")])}
{co("red","COMMON MISTAKE","Building a dynamic pivot by pasting <em>user-supplied</em> values into the SQL text. The month list above comes from your own table, but if it came from a web form, it would be an injection hole (Section 9.6). Validate values against the database, or against an allow-list, before they become identifiers. Placeholders cannot be used for column names.")}
<h3>Unpivot: wide back to long</h3>
<p>The reverse trip, one row per (category, quarter), is needed whenever a spreadsheet-style table must be loaded into a tidy fact table or plotted. The portable way is one <code>SELECT</code> per column joined by <code>UNION ALL</code>:</p>
{P("7.4.3","Turn the wide <code>targets</code> table (one column per quarter) into a long table. Predict first: 2 categories x 3 quarters = 6 rows.")}
{unp}
{steps([("Step 1","Each <code>SELECT</code> reads one wide column and writes its name as text in the <code>quarter</code> column."),("Step 2","Six rows come back, as predicted: 2 categories times 3 quarters."),("Native forms","SQL Server and Oracle write <code>UNPIVOT (target FOR quarter IN (q1, q2, q3))</code>. PostgreSQL writes <code>CROSS JOIN LATERAL (VALUES ('q1', q1), ('q2', q2), ('q3', q3)) AS v(quarter, target)</code>. BigQuery has <code>UNPIVOT</code>. Snowflake has <code>UNPIVOT</code> too. None of these four were run here.")])}
<p>SQLite can also do it by expanding a JSON object, which scales to many columns without repeating the pattern. It returns the same six rows:</p>
{js}
{co("green","GOING DEEPER","A pivot is a <code>GROUP BY</code> with an aggregate per output column, so it is only correct when each (row key, column key) pair has <em>at most one</em> source row or you intend to aggregate duplicates. If the long table has two rows for (Home, 2024-02), <code>SUM</code> silently adds them and <code>MAX</code> silently drops one. Before pivoting, check uniqueness: <code>SELECT category, month, count(*) FROM sales GROUP BY 1, 2 HAVING count(*) &gt; 1</code>. Wide tables are for people and charts; keep storage and joins long.")}
<h3>Practice with answers</h3>
{qa("7.4.4","A report needs revenue per (region, product) with a subtotal per region only and a grand total, but no per-product subtotal across regions. Which operator? <em>(easy)</em>","<code>ROLLUP (region, product)</code> gives (region, product), (region) and the grand total, which is exactly this. <code>CUBE</code> would add a per-product-across-regions row set you do not want.")}
{qa("7.4.5","<code>ROLLUP (a, b, c)</code> on 2 x 3 x 4 distinct combinations, all present, how many rows? <em>(medium)</em>","Levels: (a,b,c) = 24, (a,b) = 6, (a) = 2, () = 1. Total 24 + 6 + 2 + 1 = 33.")}
{qa("7.4.6","A teammate writes the hand-made rollup with <code>UNION</code> instead of <code>UNION ALL</code>. Name two problems. <em>(find the bug)</em>","First, <code>UNION</code> removes duplicate rows, so any two branches that happen to produce an identical row (same labels, same amount) would silently lose one, and the totals would no longer add up. Second, <code>UNION</code> must sort or hash all rows to find duplicates, which costs time for nothing. Use <code>UNION ALL</code> whenever you know the branches do not overlap.")}
'''
insert("07","lab7",body)
