# ---------- 3.11 going deeper ----------
db2=shop()
def X2(code): return exec_sql(db2,code)
q1=X2("""EXPLAIN QUERY PLAN
SELECT status, COUNT(*) AS n FROM orders GROUP BY status;""")
q2=X2("""CREATE INDEX idx_orders_status ON orders(status);
EXPLAIN QUERY PLAN
SELECT status, COUNT(*) AS n FROM orders GROUP BY status;""")
q3=X2("""EXPLAIN QUERY PLAN
SELECT o.customer_id, SUM(oi.qty * oi.unit_price) AS spent
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY o.customer_id;""")
n1=X("""SELECT COUNT(*) AS rows_, COUNT(DISTINCT coupon) AS distinct_non_null FROM orders;""")
n2=X("""SELECT DISTINCT coupon FROM orders ORDER BY coupon;""")
n3=X("""SELECT coupon, COUNT(*) FROM orders GROUP BY coupon;""")
n4=X("""SELECT COUNT(*) AS equals_null FROM orders WHERE coupon = NULL;""")
r1=X("""SELECT category, COUNT(*) AS n_products, SUM(price) AS total_price
FROM products
GROUP BY category
UNION ALL
SELECT 'ALL CATEGORIES', COUNT(*), SUM(price)
FROM products
ORDER BY 1;""")
w1=X("""SELECT DISTINCT p.category,
       SUM(oi.qty * oi.unit_price) OVER (PARTITION BY p.category) AS category_revenue,
       SUM(oi.qty * oi.unit_price) OVER ()                         AS grand_total
FROM order_items oi JOIN products p ON p.product_id = oi.product_id
ORDER BY p.category;""")
w2=X("""SELECT oi.order_id, oi.product_id, oi.qty * oi.unit_price AS line_total,
       SUM(oi.qty * oi.unit_price) OVER (PARTITION BY oi.order_id) AS order_total
FROM order_items oi
WHERE oi.order_id IN (101, 103)
ORDER BY oi.order_id, oi.product_id;""")
c1=X("""SELECT 0.1 + 0.2 AS sum_float, (0.1 + 0.2) = 0.3 AS equals_point3,
       ROUND(0.1 + 0.2, 2) = 0.3 AS rounded_equals;""")
py1=pyblock('''
import pandas as pd
import numpy as np
marks = pd.DataFrame({
    "student": ["Asha","Asha","Ravi","Ravi","Meena","Meena","John","John"],
    "subject": ["maths","science","maths","science","maths","science","maths","science"],
    "mark":    [78, 85, 62, np.nan, 91, 74, 55, 68],
})
g = marks.groupby("subject")["mark"]
print(g.agg(n_rows="size", n_marks="count", total="sum", avg="mean", lo="min", hi="max"))
print()
print("sum of an all-NaN group:", pd.Series([np.nan, np.nan]).sum())
print("SQL would give NULL; pandas gives 0.0 unless min_count=1:", pd.Series([np.nan, np.nan]).sum(min_count=1))
coupon = pd.DataFrame({"coupon": ["SAVE10", None, None, "SAVE10", None]})
print(coupon.groupby("coupon").size().to_dict())
print(coupon.groupby("coupon", dropna=False).size().to_dict())
''')
py2=pyblock('''
# why AVG cannot be computed from partial AVGs: carry (sum, count) instead
part_a = [100]                 # one machine holds 1 row
part_b = [200, 200, 200]       # another holds 3 rows
avg_a = sum(part_a) / len(part_a)
avg_b = sum(part_b) / len(part_b)
print("average of averages:", (avg_a + avg_b) / 2)
s = sum(part_a) + sum(part_b)
n = len(part_a) + len(part_b)
print("sum of sums / sum of counts:", s / n)
''')
py3=pyblock('''
total = 0.0
for _ in range(10):
    total += 0.1
print(total, total == 1.0)
cents = sum([10] * 10)      # money in whole cents: exact
print(cents, cents / 100)
''')
body=f'''
<h2 id="x11-3-11-going-deeper">3.11 Going Deeper: Internals, Edge Cases, Performance and What Interviewers Probe</h2>
<p>This part is for when the basics feel solid. You do not need it to write correct everyday queries, but each idea here removes a class of surprises, and interviewers love them.</p>
<h3>How the database really groups</h3>
<p>The pipeline in Section 3.5 is <em>logical</em>: the order in which the meaning of the query is defined. The engine is free to do the work differently as long as the answer is the same. Two physical strategies do the grouping:</p>
<ul><li><strong>Hash aggregate.</strong> Read the rows once; keep a hash table from key to running aggregate (for example key 'paid' to running count). Memory is proportional to the number of <em>groups</em>, not rows. Fast when there are few groups.</li><li><strong>Sort (stream) aggregate.</strong> Sort the rows by key (or read them from an index that is already sorted), then walk through: when the key changes, emit a row. Needs little memory when the input is already ordered, and delivers sorted output for free.</li></ul>
<p>SQLite shows its choice with <code>EXPLAIN QUERY PLAN</code>. Without an index on <code>status</code> it builds a temporary sorted structure; with an index it reads the already-ordered index.</p>
{P("3.11.1","See the grouping strategy. Show the plan for counting orders per status, first without and then with an index on <code>status</code>.")}
{q1}
{q2}
{steps([("Step 1","Without an index the engine scans the whole table and uses a temporary B-tree to collect the groups (<code>USE TEMP B-TREE FOR GROUP BY</code>)."),("Step 2","After <code>CREATE INDEX</code> on <code>status</code> the plan scans the index only (<code>COVERING INDEX</code>), because the index already holds the statuses in sorted order. Equal keys sit next to each other, so no temporary structure is needed."),("Step 3","On 14 rows the difference is invisible. On 100 million rows the index avoids a big sort or hash table, which is where the speed comes from (Chapter 10)."),("Answer","The exact wording of plans differs between SQLite versions and between databases; the idea does not.")])}
{q3}
<p>For a grouped join, filter early. The plan above shows the engine can use the primary key of <code>order_items</code> to find the lines of each order. Whatever the join method, rows removed by <code>WHERE</code> never reach the grouping step, which is why Section 3.3 said to prefer <code>WHERE</code>.</p>
<h3>NULL: equal for grouping, unknown for comparison</h3>
<p>The database has two different notions of 'same'. In a comparison, <code>NULL = NULL</code> is unknown. In <code>GROUP BY</code>, <code>DISTINCT</code> and set operators, NULLs are treated as <em>not distinct from each other</em>, so they form one group or one row. And <code>COUNT(DISTINCT col)</code> does not count the NULL group at all.</p>
{P("3.11.2","Show the three NULL behaviours on the coupon column: the NULL group exists in <code>GROUP BY</code> and <code>DISTINCT</code>, the distinct count ignores it, and <code>= NULL</code> matches nothing.")}
{n3}
{n2}
{n1}
{n4}
{steps([("Step 1","<code>GROUP BY coupon</code> shows a NULL group of 11 rows and a SAVE10 group of 3."),("Step 2","<code>DISTINCT coupon</code> lists NULL and SAVE10: NULLs collapse into one row."),("Step 3","<code>COUNT(DISTINCT coupon)</code> is 1: aggregates skip NULL, so the NULL 'value' is not counted."),("Step 4","<code>WHERE coupon = NULL</code> matches 0 rows. The correct test is <code>IS NULL</code>."),("Meaning","If you need the NULL group counted as a kind, use <code>COUNT(DISTINCT COALESCE(coupon, '(none)'))</code>, which gives 2.")])}
<h3>Aggregates can be combined in pieces (and some cannot)</h3>
<p>Big engines (Spark, BigQuery, Snowflake, Redshift, ClickHouse) split data across many machines. Each machine computes a <em>partial</em> aggregate over its slice and a final step merges them. That works for <code>SUM</code>, <code>COUNT</code>, <code>MIN</code>, <code>MAX</code>. It works for <code>AVG</code> only if each machine sends <code>(sum, count)</code> and the final step divides. It fails for the median and exact distinct counts, which need all the values or a sketch. This is the same reason you cannot average averages.</p>
{py2}
<p>The average of averages is 150.0 but the correct answer is 175.0: 100 + 200 + 200 + 200 = 700 over 4 rows. This is Problem 3.P.10 in code. Because exact <code>COUNT(DISTINCT)</code> is expensive at scale, warehouses offer approximate versions (<code>APPROX_COUNT_DISTINCT</code> in BigQuery, Snowflake and Spark; <code>approx_distinct</code> in Trino) that use a sketch called HyperLogLog and are accurate to about one or two percent with tiny memory. Use them when a dashboard needs speed and tolerates a small error; never for billing.</p>
<h3>Numbers: floats, money and overflow</h3>
{P("3.11.3","(expert) Floating-point surprises. Check whether 0.1 + 0.2 equals 0.3 in SQL, and how to compare safely.")}
{c1}
{py3}
{steps([("Step 1","Decimal fractions like 0.1 have no exact binary form, so the sum is 0.30000000000000004 and the equality is false (0)."),("Step 2","Rounding to 2 decimals first makes the comparison true."),("Step 3","Adding 0.1 ten times, one addition at a time, gives 0.9999999999999999, not 1.0. Some engines (and Python's own <code>sum</code> in recent versions) compensate for this inside the function, others do not, so do not depend on it."),("Step 4","Money should be stored as integer cents or a fixed-point <code>DECIMAL(p, s)</code> column. The shop stores whole rupees, so its sums are exact."),("Answer","Never test floats for equality in HAVING or WHERE; round, or compare with a small tolerance.")])}
{co("red","COMMON MISTAKE","Trusting the type of an aggregate. In SQL Server and some others <code>SUM</code> of an <code>INT</code> column returns an <code>INT</code> and can overflow on large tables (cast to <code>BIGINT</code> first). In PostgreSQL <code>SUM</code> of <code>INT</code> returns <code>BIGINT</code>, and <code>AVG</code> of integers returns a decimal. SQLite raises an 'integer overflow' error when a sum of integers exceeds 64 bits. Know your engine's rule before summing billions.")}
<h3>SQL aggregation versus pandas aggregation</h3>
<p>If you move between SQL and pandas, three differences cause silent bugs.</p>
{py1}
{steps([("Step 1","<code>size</code> counts rows (like <code>COUNT(*)</code>), <code>count</code> counts non-missing values (like <code>COUNT(col)</code>). The science line shows 4 and 3."),("Step 2","The sum of an all-missing group is <code>0.0</code> in pandas, but NULL in SQL. Pass <code>min_count=1</code> to get the SQL behaviour."),("Step 3","<code>groupby</code> drops missing keys by default, so the coupon-less rows vanish and you see only SAVE10: 2. SQL keeps the NULL group. Pass <code>dropna=False</code> to keep it (pandas shows it under key <code>nan</code>)."),("Meaning","When you check a pandas result against SQL, compare these three behaviours first.")])}
<h3>Subtotals and grand totals</h3>
<p>Reports often want group rows <em>and</em> a total row. PostgreSQL, MySQL, SQL Server and Oracle have <code>GROUP BY ROLLUP (category)</code> and <code>GROUPING SETS</code>, covered in Chapter 7. SQLite has neither, but <code>UNION ALL</code> gives the same result: one grouped query stacked on a one-row total query.</p>
{P("3.11.4","Products and total price per category with a grand total row.")}
{r1}
{steps([("Step 1","The first query has grain 'one row per category'; the second has grain 'one row'. <code>UNION ALL</code> stacks them because both have three columns of the same kinds."),("Step 2","The literal 'ALL CATEGORIES' fills the label column of the total row."),("Step 3","<code>ORDER BY 1</code> sorts by the first column, which puts 'ALL CATEGORIES' first alphabetically. For a total at the bottom, add a sort column (0 for groups, 1 for the total)."),("Check","2 + 2 + 2 = 6 products and 3450 total price, equal to the grand total row.")])}
<pre class="code lang-sql"><code>-- PostgreSQL / MySQL 8 / SQL Server / Oracle (not run here: SQLite has no ROLLUP)
SELECT category, COUNT(*) AS n_products, SUM(price) AS total_price
FROM products
GROUP BY ROLLUP (category);</code></pre>
<p>Expected output in those databases: the three category rows plus one extra row where <code>category</code> is NULL, with 6 and 3450. Use <code>GROUPING(category)</code> to tell that NULL from a real NULL category.</p>
<h3>Aggregate versus window: keep the rows</h3>
<p>An aggregate collapses rows. A <em>window</em> aggregate (<code>SUM(...) OVER (...)</code>) computes the same number but keeps every row, so you can put the group total beside each detail row. Chapter 8 teaches windows in full; here is a preview so you can see the difference.</p>
{P("3.11.5","Show each line of orders 101 and 103 next to its order total, without collapsing the lines.")}
{w2}
{steps([("Step 1","<code>PARTITION BY order_id</code> is the window's <code>GROUP BY</code>: it makes the piles."),("Step 2","But every input row is kept. Order 101's two lines (1500 and 160) both show the order total 1660; order 103's lines (900, 120) both show 1020."),("Meaning","Use <code>GROUP BY</code> when the answer has one row per group. Use a window when you need detail and group figures side by side (percent of total, rank within group, running totals).")])}
{w1}
<p>The same window syntax gives the grand total column without a scalar subquery. <code>OVER ()</code> means 'one pile: the whole result'.</p>
<h3>Dialect cheat table</h3>
{tbl(["Feature","SQLite","PostgreSQL","MySQL","SQL Server"],[
["alias in GROUP BY","yes","yes","yes","no"],
["alias in HAVING","yes","no","yes","no"],
["non-grouped column in SELECT","allowed (arbitrary row)","error","error unless ONLY_FULL_GROUP_BY is off (on by default since 5.7)","error"],
["<code>FILTER (WHERE ...)</code>","3.30+","9.4+","no (use CASE)","no (use CASE)"],
["integer <code>/</code> integer","integer","integer","decimal","integer"],
["string list aggregate","<code>group_concat</code>","<code>string_agg</code>","<code>GROUP_CONCAT</code>","<code>STRING_AGG</code> (2017+)"],
["<code>ROLLUP</code>","no","yes","yes (<code>WITH ROLLUP</code>)","yes"],
["division by zero","NULL","error","NULL (usually)","error"]])}
<p>Treat the table as a guide for what to look up first, not a guarantee: versions and settings change behaviour.</p>
<h3>Performance rules of thumb</h3>
<ul><li>Filter with <code>WHERE</code> before grouping, and filter on indexed, sargable conditions (Chapter 10).</li><li>Aggregate to the needed grain <em>before</em> joining to other large tables (Section 3.7): joining 14 order totals is cheaper and safer than joining 20 lines.</li><li>A covering index on <code>(status)</code> or <code>(customer_id, status)</code> can answer a grouped count without touching the table.</li><li><code>COUNT(*)</code>, <code>COUNT(1)</code> mean the same thing. <code>COUNT(col)</code> is not the same as <code>COUNT(*)</code> when col has NULLs, regardless of speed.</li><li><code>COUNT(DISTINCT x)</code> needs a sort or hash set of x; on huge data try a sketch or a pre-aggregated table.</li><li><code>HAVING</code> cannot use an index on the aggregate; if a threshold is needed often, store the pre-aggregated table (a summary table or materialised view).</li></ul>
<h3>What interviewers probe</h3>
{tbl(["Question","Short strong answer"],[
["WHERE versus HAVING?","WHERE filters rows before grouping and cannot use aggregates; HAVING filters groups after aggregation."],
["COUNT(*) versus COUNT(col) versus COUNT(DISTINCT col)?","rows; non-NULL values; different non-NULL values."],
["What does SUM return on no rows?","NULL, while COUNT returns 0; COALESCE if you need 0."],
["Why is average of averages wrong?","It weights groups equally regardless of size. Carry sum and count, divide once."],
["How do you find duplicates?","GROUP BY the key HAVING COUNT(*) &gt; 1; or COUNT(*) - COUNT(DISTINCT key)."],
["How do you pivot without PIVOT?","One FILTER or CASE aggregate per output column."],
["Your count doubled after a join. Why?","Fan-out from a one-to-many join; aggregate first or COUNT(DISTINCT key)."],
["Order of evaluation of a query?","FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, LIMIT."],
["How is NULL handled in GROUP BY?","All NULLs form a single group."],
["Can you use a SELECT alias in WHERE?","Not in standard SQL (SELECT runs later); some engines allow it, do not rely on it."]])}
<div class="callout cream"><div class="lab">INTERVIEW</div><div class="txt">Interviewers often give a small table and ask for a result by hand. Practise the habit from this chapter: write the grain, draw the piles on paper, compute each pile, then write the SQL. The answer you derive by hand is also the answer you check the query against.</div></div>
'''
ins("d7",body)
