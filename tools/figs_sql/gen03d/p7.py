# ---------- 3.12 drill, 3.13 self-test, 3.14 where next ----------
def QA(code,q,sqlcode,ans):
    return P(code,q)+"\n"+X(sqlcode)+"\n<p><strong>Answer:</strong> "+ans+"</p>"
d1=QA("3.12.1","(warm-up) Which orders have two or more item lines?","""SELECT order_id, COUNT(*) AS n_lines
FROM order_items
GROUP BY order_id
HAVING COUNT(*) >= 2
ORDER BY order_id;""","Orders 101, 103, 106, 110, 113 and 114, two lines each. Grain: one row per order. The condition counts lines, so it is a pile condition: HAVING.")
d2=QA("3.12.2","Units bought in paid orders, per customer name, largest first.","""SELECT c.name, SUM(oi.qty) AS units
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id   = o.order_id
WHERE o.status = 'paid'
GROUP BY c.customer_id, c.name
ORDER BY units DESC, c.name;""","Asha 9, Priya 7, Kabir 5, Ravi 4, John 3, total 28. Check: total units are 34; the 6 units in the cancelled and refunded orders (5 notebooks in order 104 and 1 keyboard in order 109) are excluded, and 34 - 6 = 28. Meena has only a cancelled order and so is absent.")
d3=QA("3.12.3","Average line total per category, rounded to 1 decimal.","""SELECT p.category, ROUND(AVG(oi.qty * oi.unit_price), 1) AS avg_line
FROM order_items oi JOIN products p ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY p.category;""","Electronics 1125.0 (9000 / 8 lines), Home 1200.0 (3600 / 3), Stationery 217.8 (1960 / 9). Each is a sum divided by the count of lines in that same pile, so it is a legitimate average.")
d4=QA("3.12.4","Paid orders split by coupon use: number of orders, revenue and average order value. Pre-aggregate lines to orders first.","""WITH order_totals AS (
  SELECT order_id, SUM(qty * unit_price) AS total FROM order_items GROUP BY order_id
)
SELECT COALESCE(o.coupon, '(none)') AS coupon, COUNT(*) AS n_orders,
       SUM(t.total) AS revenue, ROUND(AVG(t.total), 1) AS aov
FROM orders o JOIN order_totals t ON t.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY o.coupon;""","No coupon: 9 orders, 10120, AOV 1124.4. SAVE10: 3 orders, 2540, AOV 846.7. Check: 9 + 3 = 12 orders and 10120 + 2540 = 12660. Coupon orders are smaller by about 25 percent, a finding worth a note (with only 3 orders, do not over-read it).")
d5=QA("3.12.5","Which months had at least one order that was not paid?","""SELECT substr(order_date,1,7) AS month,
       COUNT(*) FILTER (WHERE status <> 'paid') AS not_paid
FROM orders
GROUP BY month
HAVING COUNT(*) FILTER (WHERE status <> 'paid') > 0
ORDER BY month;""","February (the cancelled order 104) and March (the refunded order 109), one each. January and April have none and are dropped by HAVING.")
d6=QA("3.12.6","Customers whose first order was in January 2024.","""SELECT customer_id, MIN(order_date) AS first_order
FROM orders
GROUP BY customer_id
HAVING MIN(order_date) &lt; '2024-02-01'
ORDER BY customer_id;""".replace("&lt;","<"),"Customer 1 (2024-01-10) and customer 2 (2024-01-15). ISO text dates compare correctly as strings. A WHERE version (<code>WHERE order_date &lt; '2024-02-01'</code>) gives the same two customers on this data, but it answers 'who ordered before February', which is a different question and differs as soon as older data exists.")
d7=QA("3.12.7","The three customers who bought the most different products in paid orders.","""SELECT o.customer_id, COUNT(DISTINCT oi.product_id) AS kinds
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY o.customer_id
ORDER BY kinds DESC, o.customer_id
LIMIT 3;""","Customer 1 with 5 products (everything but the Mug), customer 2 with 3 (Mouse, Desk Lamp, Keyboard), customer 4 with 2 (Keyboard, Desk Lamp). Tie-break by customer id keeps the output deterministic. Customers 5 and 6 have 2 and 2 as well, so the cut at 3 rows decides by id; note this in a report.")
d8=QA("3.12.8","What percent of all units sold are Notebooks?","""SELECT ROUND(100.0 * SUM(qty) FILTER (WHERE product_id = 3) / SUM(qty), 1) AS pct_notebook_units
FROM order_items;""","14 of 34 units, 41.2 percent. Both the numerator and denominator come from the same pile (all lines), so one pass with FILTER is enough. Note that Notebooks are only 7.7 percent of revenue (1120 / 14560): units and money tell different stories.")
body=f'''
<h2 id="x12-3-12-mixed-practice-drill">3.12 Mixed-Practice Drill</h2>
<p>Do these without looking at the answers. For each, write the grain first, then the query, then check it against a total you know (14560 revenue, 12660 paid, 34 units, 20 lines, 14 orders). Compare with the output and the answer below it.</p>
{d1}
{d2}
{d3}
{d4}
{d5}
{d6}
{d7}
{d8}
<p><strong>Scoring yourself.</strong> Count a problem as correct only if your query returned the shown result without edits. 8 of 8: move on. 6 or 7: reread the section named in the playbook table for the ones you missed. 5 or fewer: redo Sections 3.7 to 3.9 and rerun every example by hand.</p>
<h2 id="x13-3-13-self-test-and-scoring-guide">3.13 Self-Test and Scoring Guide</h2>
<p>Fifteen short questions, one point each. Answer in your head or on paper first, then read the answer under each.</p>
<ol>
<li>What does <code>SELECT SUM(qty) FROM order_items WHERE qty &gt; 100</code> return? <br/><strong>Answer:</strong> One row containing NULL (not 0, not no rows).</li>
<li>A column has values 4, 6, NULL. What are <code>COUNT(*)</code>, <code>COUNT(col)</code> and <code>AVG(col)</code>? <br/><strong>Answer:</strong> 3, 2 and 5.0.</li>
<li>Why does <code>SUM(qty) / COUNT(*)</code> give 1 for 34 units over 20 lines in SQLite? <br/><strong>Answer:</strong> Integer division truncates 1.7 to 1. Multiply by <code>1.0</code>.</li>
<li>Which clause can contain <code>COUNT(*) &gt; 2</code>: WHERE or HAVING? <br/><strong>Answer:</strong> HAVING.</li>
<li>Where do you put <code>status = 'paid'</code> for speed and clarity? <br/><strong>Answer:</strong> WHERE.</li>
<li>Why is the average of customer averages (962) not the AOV (1055)? <br/><strong>Answer:</strong> Customers with more orders deserve more weight; divide total revenue by total orders.</li>
<li>What is the grain of <code>SELECT month, category, SUM(x) ... GROUP BY month, category</code>? <br/><strong>Answer:</strong> One row per month and category that occurs in the data.</li>
<li>After joining orders to order_items, what does <code>COUNT(*)</code> count? <br/><strong>Answer:</strong> Item lines. Use <code>COUNT(DISTINCT order_id)</code> for orders.</li>
<li>How do GROUP BY and DISTINCT treat NULLs? <br/><strong>Answer:</strong> All NULLs form one group or one row.</li>
<li>Why is <code>COUNT(CASE WHEN c THEN 1 ELSE 0 END)</code> wrong? <br/><strong>Answer:</strong> 0 is not NULL, so every row is counted.</li>
<li>Write a portable replacement for <code>SUM(x) FILTER (WHERE y = 1)</code>. <br/><strong>Answer:</strong> <code>SUM(CASE WHEN y = 1 THEN x END)</code>.</li>
<li>How do you avoid division by zero in a rate? <br/><strong>Answer:</strong> Divide by <code>NULLIF(denominator, 0)</code>; the result is NULL when undefined.</li>
<li>How do you list customers with <em>no</em> paid order, including those with no orders at all? <br/><strong>Answer:</strong> LEFT JOIN from customers, group by customer, <code>HAVING COUNT(*) FILTER (WHERE o.status='paid') = 0</code>.</li>
<li>Per-product revenue sums to 14500 but the plain total is 14560. What do you check first? <br/><strong>Answer:</strong> Rows lost by an inner join or a WHERE (here 60 is missing), or rows with NULL keys that your grouping dropped.</li>
<li>Name two ways to get the whole row (the name) of the maximum in each group. <br/><strong>Answer:</strong> Join back to a subquery of the group maximum; or number rows with <code>ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ... DESC)</code> and keep 1.</li>
</ol>
{tbl(["Score","What it means","What to reread"],[
["14 to 15","Solid. You can solve most grouped-query problems.","Do the practice set under time pressure; then Chapter 4 (joins)."],
["11 to 13","Good, with a few leaks.","Reread the sections for the questions you missed: 1 to 3 and 12: Section 3.6; 4, 5 and 14: Sections 3.5 and 3.8; 7 to 9 and 13: Section 3.7; 10 and 11: Section 3.9; 15: Section 3.10."],
["7 to 10","Shaky on the mechanics.","Reread Sections 3.5 to 3.9 slowly, running every example. Redo the drill."],
["0 to 6","Start again from the pipeline.","Read Section 3.5 and Problem 3.5.1 until you can draw the pipeline from memory, then redo Sections 3.1 to 3.4 with a pencil."]])}
<h2 id="x14-3-14-where-this-chapter-sits">3.14 Where This Chapter Sits: What Came Before and What Comes Next</h2>
<ul><li><strong>Before (Chapter 2).</strong> Chapter 2 gave you <code>WHERE</code>, <code>ORDER BY</code>, <code>LIMIT</code>, <code>DISTINCT</code> and NULL logic. Every aggregate rule here rests on it: aggregates skip NULL, and <code>WHERE</code> keeps only rows where the test is true (Section 2.4).</li><li><strong>This chapter.</strong> Collapse rows into piles and numbers, and filter piles.</li><li><strong>Next (Chapter 4).</strong> Joins bring several tables together. You now know why every join changes the grain and how to guard against fan-out; Chapter 4 teaches the join types, and you will meet the aggregate-before-join cure again.</li><li><strong>Later.</strong> Chapter 5 (subqueries, CTEs, <code>EXISTS</code>) for the comparisons in Patterns 5 and 8; Chapter 7 for <code>ROLLUP</code>, <code>CUBE</code> and pivots; Chapter 8 for window functions (top-N per group, running totals, percent of total); Chapter 10 for indexes and plans; Chapter 12 for retention, funnels and cohorts built from the patterns in this chapter.</li></ul>
'''
ins("d8",body)

# ----- extra practice problems: inserted before prompt pack -----
def PQ(code,q,sqlcode,ans): return QA(code,q,sqlcode,ans)
pp=[]
pp.append(PQ("3.P.11","(easy) How many products cost more than 100, and how many per category?","""SELECT category, COUNT(*) AS n
FROM products
WHERE price > 100
GROUP BY category
ORDER BY category;""","Electronics 2, Home 2, Stationery 1 (the Pen Pack at 120; the Notebook at 80 is excluded). Total 5. WHERE is right because price is a row-level fact."))
pp.append(PQ("3.P.12","(easy) The latest order date for every customer.","""SELECT customer_id, MAX(order_date) AS last_order
FROM orders
GROUP BY customer_id
ORDER BY customer_id;""","Customer 1: 2024-04-02, 2: 2024-04-20, 3: 2024-02-10, 4: 2024-04-09, 5: 2024-04-15, 6: 2024-03-30. Six rows because only six customers ever ordered."))
pp.append(PQ("3.P.13","(what is the output?) Predict the three numbers, then run.","""SELECT COUNT(*), COUNT(coupon), SUM(coupon IS NULL) FROM orders;""","14, 3 and 11. <code>coupon IS NULL</code> is 1 for orders without a coupon and 0 otherwise (SQLite and MySQL treat comparisons as 0/1), so summing it counts them: 14 - 3 = 11. In PostgreSQL write <code>COUNT(*) FILTER (WHERE coupon IS NULL)</code>."))
pp.append(PQ("3.P.14","(find the bug) A teammate wants customers with more than 2 paid orders and writes the query below. What does it return, and why is it wrong?","""SELECT customer_id, COUNT(*)
FROM orders
WHERE status = 'paid'
HAVING COUNT(*) > 2;""","It returns a single row, customer 1 with 12, which is silently wrong: there is no GROUP BY, so all 12 paid orders form one pile, and SQLite fills the bare <code>customer_id</code> from an arbitrary row. PostgreSQL would refuse (column must appear in GROUP BY). Fix: add <code>GROUP BY customer_id</code>; the result is customers 1 (4), 2 (3) only."))
pp.append(PQ("3.P.15","(medium) Average units per paid order for each customer (units divided by distinct orders).","""SELECT o.customer_id,
       COUNT(DISTINCT o.order_id) AS orders,
       SUM(oi.qty)                AS units,
       ROUND(1.0 * SUM(oi.qty) / COUNT(DISTINCT o.order_id), 2) AS units_per_order
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY o.customer_id
ORDER BY o.customer_id;""","Customer 1: 9 / 4 = 2.25; 2: 4 / 3 = 1.33; 4: 3 / 2 = 1.5; 5: 7 / 2 = 3.5; 6: 5 / 1 = 5.0. The denominator must be distinct orders, because the join produces one row per line (Section 3.7)."))
pp.append(PQ("3.P.16","(medium) Rank the months by paid revenue, highest first.","""SELECT substr(o.order_date,1,7) AS month, SUM(oi.qty * oi.unit_price) AS revenue
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY month
ORDER BY revenue DESC;""","April 4900, March 2980, February 2520, January 2260; total 12660. ORDER BY may use the aggregate alias because ORDER BY runs after SELECT."))
pp.append(PQ("3.P.17","(medium) For each category: lines, lines with two or more units, and the percent.","""SELECT p.category,
       COUNT(*) AS lines,
       COUNT(*) FILTER (WHERE oi.qty >= 2) AS multi_unit,
       ROUND(100.0 * COUNT(*) FILTER (WHERE oi.qty >= 2) / COUNT(*), 1) AS pct
FROM order_items oi JOIN products p ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY p.category;""","Electronics 8 lines, 1 multi-unit (order 106 buys 2 mice): 12.5 percent. Home 3 lines, 1 (order 112, 2 lamps): 33.3. Stationery 9 lines, 6: 66.7. Stationery is bought in multiples, as expected for cheap items. Lines add to 20."))
pp.append(PQ("3.P.18","(hard) Customers for whom at least one third of their orders were refunded.","""SELECT customer_id, COUNT(*) AS orders,
       COUNT(*) FILTER (WHERE status = 'refunded') AS refunded
FROM orders
GROUP BY customer_id
HAVING 3.0 * COUNT(*) FILTER (WHERE status = 'refunded') >= COUNT(*);""","Only customer 5 (1 refunded of 3). The test is written as <code>3 * refunded &gt;= orders</code> instead of <code>refunded / orders &gt;= 1/3</code> to avoid a division and a rounding error on 0.3333. Cross-multiplying is a good habit for ratio thresholds."))
pp.append(PQ("3.P.19","(hard) Who bought from all three categories? Count the categories per customer and keep the customers that reach 3.","""SELECT o.customer_id, COUNT(DISTINCT p.category) AS categories
FROM orders o
JOIN order_items oi ON oi.order_id  = o.order_id
JOIN products    p  ON p.product_id = oi.product_id
GROUP BY o.customer_id
HAVING COUNT(DISTINCT p.category) = 3;""","Only customer 1. A 'bought every one of N things' question is <code>HAVING COUNT(DISTINCT thing) = N</code> where N is the total number of things (here 3; check it with <code>SELECT COUNT(DISTINCT category) FROM products</code> rather than hard-coding). All orders count here, including the cancelled one."))
pp.append(PQ("3.P.20","(hard) Each customer's share of paid revenue, largest first.","""SELECT o.customer_id,
       SUM(oi.qty * oi.unit_price) AS spent,
       ROUND(100.0 * SUM(oi.qty * oi.unit_price) /
             (SELECT SUM(i2.qty * i2.unit_price)
              FROM orders o2 JOIN order_items i2 ON i2.order_id = o2.order_id
              WHERE o2.status = 'paid'), 1) AS pct
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY o.customer_id
ORDER BY spent DESC;""","Customer 1 36.0 percent, 2 28.4, 4 26.1, 5 6.0, 6 3.5; 36.0 + 28.4 + 26.1 + 6.0 + 3.5 = 100.0. The subquery repeats the same WHERE as the outer query: a share is only meaningful if numerator and denominator use the same filter."))
pp.append(PQ("3.P.21","(hard) New buyers per month: customers whose first paid order falls in that month.","""SELECT substr(first_paid, 1, 7) AS month, COUNT(*) AS new_buyers
FROM (SELECT customer_id, MIN(order_date) AS first_paid
      FROM orders
      WHERE status = 'paid'
      GROUP BY customer_id)
GROUP BY month
ORDER BY month;""","January 2 (customers 1 and 2), February 1 (customer 4), March 2 (customers 5 and 6), April 0 (no row). Total 5 paying customers. This is a two-level aggregation: first one row per customer, then one row per month. Two levels solve most cohort questions."))
pp.append(PQ("3.P.22","(expert) A dashboard shows average order value as <code>AVG(qty * unit_price)</code> over <code>order_items</code>. Is it right? Compare with revenue divided by the number of orders (all statuses).","""SELECT ROUND(AVG(qty * unit_price), 1) AS avg_line_value,
       ROUND(1.0 * SUM(qty * unit_price) / COUNT(DISTINCT order_id), 1) AS aov_all_orders
FROM order_items;""","No. <code>AVG</code> over lines gives 728.0, the average <em>line</em>. The AOV is revenue per <em>order</em>: 14560 / 14 = 1040.0. The dashboard understates AOV by 30 percent because orders have 1.43 lines on average (20 / 14). Match the grain of the average to the noun in its name."))
pp.append(PQ("3.P.23","(expert) Customers who ordered in at least 2 different months (a simple repeat-over-time test).","""SELECT customer_id,
       COUNT(DISTINCT substr(order_date, 1, 7)) AS active_months,
       COUNT(*) AS orders
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT substr(order_date, 1, 7)) >= 2
ORDER BY customer_id;""","Customer 1 (4 months), 2 (3), 4 (2: February and April) and 5 (2: March and April). Customer 3 and 6 ordered once. Counting months, not orders, matters: a customer with 5 orders in one day is one active month."))
pp.append(PQ("3.P.24","(expert) Build a complete month-by-category grid for Home with zeros for missing months. Missing groups need a driver table that lists every month.","""WITH months(m) AS (VALUES ('2024-01'), ('2024-02'), ('2024-03'), ('2024-04')),
sales AS (
  SELECT substr(o.order_date,1,7) AS m, SUM(oi.qty * oi.unit_price) AS rev
  FROM orders o
  JOIN order_items oi ON oi.order_id  = o.order_id
  JOIN products    p  ON p.product_id = oi.product_id
  WHERE o.status = 'paid' AND p.category = 'Home'
  GROUP BY m
)
SELECT months.m AS month, COALESCE(sales.rev, 0) AS home_revenue
FROM months LEFT JOIN sales ON sales.m = months.m
ORDER BY months.m;""","January 0, February 900, March 900, April 1800. A plain GROUP BY cannot produce January because no row exists for it. The month list comes from a driver table and the aggregate is joined on with LEFT JOIN, then COALESCE turns the NULL into 0 (Pattern 2 of Section 3.10)."))
pp.append(P("3.P.25","(expert, pandas) Translate to pandas: the number of rows, the number of non-missing marks and the total mark per subject, keeping missing as missing. Data are the <code>marks</code> table. Predict first which pandas function matches <code>COUNT(*)</code>."))
pp.append(pyblock('''
import pandas as pd
import numpy as np
marks = pd.DataFrame({
    "subject": ["maths","science","maths","science","maths","science","maths","science"],
    "mark":    [78, 85, 62, np.nan, 91, 74, 55, 68],
})
out = marks.groupby("subject").agg(
    n_rows=("mark", "size"),
    n_marks=("mark", "count"),
    total=("mark", lambda s: s.sum(min_count=1)),
)
print(out)
'''))
pp.append("<p><strong>Answer:</strong> <code>size</code> matches <code>COUNT(*)</code>, <code>count</code> matches <code>COUNT(col)</code>, and <code>sum(min_count=1)</code> reproduces SQL's NULL for an all-missing group. Maths: 4, 4, 286; science: 4, 3, 227, the same as Problem 3.5.2.</p>")
pp.append(P("3.P.26","(expert, interview) You are given a 2-billion-row <code>events(user_id, event_date, event_type)</code> table in a warehouse and asked for the number of distinct users per day. The query is slow. What do you try, in order?")+"\n<p><strong>Answer:</strong> (1) Filter dates with <code>WHERE</code> first so only needed partitions are read. (2) Check that <code>event_date</code> is the partition or clustering key. (3) Replace the exact <code>COUNT(DISTINCT user_id)</code> by the engine's approximate function (<code>APPROX_COUNT_DISTINCT</code>) if one or two percent error is acceptable. (4) Pre-aggregate once to one row per (day, user) into a summary table, then count rows in it: the expensive de-duplication is paid once, not on every query. (5) Never fix it with <code>SUM(DISTINCT ...)</code> or by sampling without saying so. Explain the trade-off between exactness and cost; that is the point of the question.</p>")
pp.append(P("3.P.27","(expert, design) A report must show, for each customer, orders, paid revenue, and refund rate, in one row, even for customers with no orders. Write it with the grain stated.")+"\n"+X("""-- grain: one row per customer (8 rows)
WITH order_totals AS (
  SELECT order_id, SUM(qty * unit_price) AS total FROM order_items GROUP BY order_id
)
SELECT c.customer_id, c.name,
       COUNT(o.order_id)                                        AS orders,
       COALESCE(SUM(t.total) FILTER (WHERE o.status = 'paid'), 0) AS paid_revenue,
       ROUND(1.0 * COUNT(*) FILTER (WHERE o.status = 'refunded')
             / NULLIF(COUNT(o.order_id), 0), 2)                 AS refund_rate
FROM customers c
LEFT JOIN orders o        ON o.customer_id = c.customer_id
LEFT JOIN order_totals t  ON t.order_id    = o.order_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;""")+"\n<p><strong>Answer:</strong> Orders are counted with <code>COUNT(o.order_id)</code> so Sana and Tom show 0 (not 1). Pre-aggregating to order totals keeps the join at order grain so nothing is double counted. <code>COALESCE</code> turns the NULL sum into 0 for customers without paid revenue. The refund rate divides by <code>NULLIF(orders, 0)</code>, so Sana and Tom show NULL (undefined), and customer 5 shows 0.33. Reconcile: paid revenue column adds to 12660; orders column to 14. One subtle point: <code>COUNT(*) FILTER</code> counts the placeholder row, but the filter on status removes it since its status is NULL.</p>")
insert_before(PROMPT,"d9","\n".join(pp))
