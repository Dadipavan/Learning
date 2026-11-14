# ---------- 3.7 GROUP BY in depth ----------
g1=X("""SELECT c.customer_id, c.name,
       COUNT(*)          AS wrong_count_star,
       COUNT(o.order_id) AS right_n_orders
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;""")
g2=X("""SELECT substr(o.order_date,1,7) AS month, p.category,
       SUM(oi.qty * oi.unit_price)   AS paid_revenue
FROM orders o
JOIN order_items oi ON oi.order_id   = o.order_id
JOIN products    p  ON p.product_id  = oi.product_id
WHERE o.status = 'paid'
GROUP BY month, p.category
ORDER BY month, p.category;""")
g3a=X("""SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY status;""")
g3b=X("""SELECT status, COUNT(*) AS n FROM orders GROUP BY 1 ORDER BY 1;""")
g4=X("""SELECT COALESCE(coupon, '(none)') AS coupon_used,
       COUNT(*) AS n_orders,
       COUNT(*) FILTER (WHERE status = 'paid') AS n_paid
FROM orders
GROUP BY coupon
ORDER BY n_orders DESC;""")
g5=X("""SELECT category, name, COUNT(*) AS n
FROM products
GROUP BY category
ORDER BY category;""")
g5b=X("""SELECT category, MAX(price) AS top_price, name
FROM products
GROUP BY category
ORDER BY category;""")
g6=X("""SELECT DISTINCT status FROM orders ORDER BY status;""")
g7=X("""SELECT c.customer_id,
       COUNT(*)                    AS rows_after_join,
       COUNT(DISTINCT o.order_id)  AS real_orders
FROM customers c
JOIN orders      o  ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id   = o.order_id
GROUP BY c.customer_id
ORDER BY c.customer_id;""")
g8=X("""WITH order_totals AS (
  SELECT order_id, SUM(qty * unit_price) AS total
  FROM order_items
  GROUP BY order_id
)
SELECT c.city,
       COUNT(*)      AS paid_orders,
       SUM(t.total)  AS paid_revenue,
       ROUND(1.0 * SUM(t.total) / COUNT(*), 1) AS aov
FROM customers c
JOIN orders o        ON o.customer_id = c.customer_id
JOIN order_totals t  ON t.order_id    = o.order_id
WHERE o.status = 'paid'
GROUP BY c.city
ORDER BY c.city;""")
g8b=X("""SELECT c.city,
       COUNT(*) AS wrong_orders,
       SUM(oi.qty * oi.unit_price) AS revenue_ok_but_count_wrong
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id   = o.order_id
WHERE o.status = 'paid'
GROUP BY c.city
ORDER BY c.city;""")
body=f'''
<h2 id="x7-3-7-group-by-in-depth">3.7 GROUP BY in Depth: Grain, Several Keys, NULL Groups and Fan-out</h2>
{co("blue","INTUITION","Think of <code>GROUP BY</code> as a sorting machine with labelled bins. You choose the label (the key). Every row drops into the bin with its label. The result has exactly one row per bin that received at least one row. So the first thing to decide is never 'which function' but 'what is one row of my answer'. That sentence is the <strong>grain</strong>.")}
{fig("ch03d_piles.png","Five stacks of coloured blocks, one stack per product, with block values, next to a horizontal bar chart of the five sums totalling 14560","Left: the 20 order lines of the shop sorted into five piles by product. Right: the sum of each pile.","each coloured block is one order line and its number is <code>qty * unit_price</code>. <code>GROUP BY product_id</code> builds the five stacks (Keyboard 4 lines, Mouse 4, Notebook 5, Pen Pack 4, Desk Lamp 3). <code>SUM</code> adds the numbers inside each stack and the bars show the result. Every block lands in exactly one stack, which is why the five bars always add up to the ungrouped total 14560.")}
<h3>Two guarantees you can rely on</h3>
<ul><li><strong>Partition.</strong> Every row goes into exactly one group. So the group counts add up to the table count, and the group sums of a column add up to the total of that column. This is your best check.</li><li><strong>Grain.</strong> The result has one row per distinct combination of key values, nothing more and nothing less. Rows with no match do not create a group, so a group with zero rows can never appear (you need a join from a table that lists all the keys, Chapter 4).</li></ul>
{P("3.7.1","(easy) How many orders has each customer placed, including customers who never ordered? Show what happens with <code>COUNT(*)</code> versus <code>COUNT(o.order_id)</code> after a <code>LEFT JOIN</code>. Predict: Sana (7) and Tom (8) have no orders.")}
{g1}
{steps([("Step 1","<code>LEFT JOIN</code> keeps every customer. A customer with no order gets one joined row with NULL in all order columns."),("Step 2","<code>COUNT(*)</code> counts that placeholder row, so Sana and Tom show 1 instead of 0."),("Step 3","<code>COUNT(o.order_id)</code> counts only non-NULL order ids, so the placeholder adds nothing: Sana and Tom show 0."),("Answer","Asha 4, Ravi 3, Meena 1, John 2, Priya 3, Kabir 1, Sana 0, Tom 0."),("Check","4 + 3 + 1 + 2 + 3 + 1 + 0 + 0 = 14, the number of orders.")])}
{co("red","COMMON MISTAKE","<code>COUNT(*)</code> after a <code>LEFT JOIN</code>. The unmatched customer still produces one row, so you report 1 order instead of 0. Count a column from the <em>right-hand</em> table (<code>COUNT(o.order_id)</code>) when you want 'how many matches'. Chapter 4 covers LEFT JOIN in full.")}
<h3>Several keys</h3>
<p>Each extra key makes the bins finer. The number of result rows is at most the product of the number of distinct values of each key, and usually far smaller because many combinations never occur.</p>
{P("3.7.2","(medium) Paid revenue by month and by category. Predict: 4 months and 3 categories could give 12 rows, but January has no Home sale.")}
{g2}
{steps([("Step 1","Grain: one row per (month, category). Join three tables to get the month (orders), the category (products) and the line total (order_items)."),("Step 2","<code>WHERE o.status = 'paid'</code> removes orders 104 and 109 first."),("Step 3","<code>GROUP BY month, p.category</code>: a pile for every pair that occurs."),("Step 4","Count the rows: Jan 2, Feb 3, Mar 3, Apr 3 = 11, not 12, because Home has no sale in January."),("Check","The 11 sums add to 12660: 2100 + 160 + 1500 + 900 + 120 + 1200 + 900 + 880 + 2700 + 1800 + 400 = 12660."),("Meaning","A missing row is not a zero. To draw a chart you need a row of 0 for (2024-01, Home); that takes a calendar-style grid joined with <code>LEFT JOIN</code>. Section 3.9 shows the pivot alternative.")])}
<h3>Ways to name the key</h3>
<p>The same grouping can be written with a column name, an expression, an alias or a position number. They produce the same piles.</p>
{g3a}
{g3b}
{tbl(["Style","Example","Works in"],[["column name","<code>GROUP BY status</code>","everywhere"],["expression","<code>GROUP BY substr(order_date,1,7)</code>","everywhere (repeat the expression in SELECT)"],["alias of a SELECT item","<code>GROUP BY month</code>","SQLite, MySQL, PostgreSQL; not SQL Server, not older Oracle"],["position number","<code>GROUP BY 1</code>","SQLite, MySQL, PostgreSQL, others; fine for quick work, fragile when you edit the column list"]])}
<p>Rule for production code: group by the real expression or column, and give the key a clear alias in <code>SELECT</code>. In daily exploration <code>GROUP BY 1, 2</code> is a harmless time-saver.</p>
<h3>NULL is a legal key</h3>
{P("3.7.3","(medium) Orders per coupon, with the number paid. Predict: coupons are SAVE10 on three orders and NULL on eleven.")}
{g4}
{steps([("Step 1","In <code>GROUP BY</code>, all NULLs are treated as equal, so the 11 orders without a coupon form one bin. (Compare with <code>WHERE coupon = NULL</code>, which is never true. Grouping uses 'same bucket', not 'equal'.)"),("Step 2","<code>COALESCE(coupon, '(none)')</code> in SELECT is only a readable label for the NULL bin. It is allowed because it is built from the grouped column alone."),("Step 3","<code>FILTER (WHERE status = 'paid')</code> counts the paid ones inside each bin: the 11 orders without a coupon include 1 cancelled and 1 refunded, so 9 paid; the 3 coupon orders are all paid."),("Check","11 + 3 = 14 orders; 9 + 3 = 12 paid, matching the 12 paid orders overall.")])}
<h3>What may appear in SELECT?</h3>
<p>Only the group keys, aggregates, constants, and expressions built from those. A plain column that is neither is ambiguous: a pile has many values of it, and the database must pick one. PostgreSQL, SQL Server and Oracle refuse such a query. SQLite and (old) MySQL accept it and pick a value from some row of the pile.</p>
{P("3.7.4","(medium) What does SQLite return for <code>SELECT category, name, COUNT(*) ... GROUP BY category</code>? Then the same with <code>MAX(price)</code>. Predict whether the name is meaningful.")}
{g5}
{g5b}
{steps([("Step 1","In the first query <code>name</code> is not grouped, not aggregated. SQLite returns the name from an arbitrary row of each pile (Keyboard, Desk Lamp, Notebook here). Another SQLite version or a different table order could return another name."),("Step 2","In the second query there is a single <code>MAX</code> or <code>MIN</code>. SQLite has a special documented rule: the bare column comes from the row that holds the max. So Keyboard (1500) and Desk Lamp (900) are correct; Pen Pack (120) is the dearest stationery item."),("Step 3","PostgreSQL rejects both: <code>column products.name must appear in the GROUP BY clause or be used in an aggregate function</code>."),("Answer","Never rely on the SQLite rule in code that must be portable. Use a window function (Chapter 8) or a join back to the max, shown in Pattern 5 of Section 3.10.")])}
<h3>GROUP BY without an aggregate is DISTINCT</h3>
{g6}
<p>That is the same answer as <code>SELECT status FROM orders GROUP BY status</code>. Use <code>DISTINCT</code> when you only need the unique values, and <code>GROUP BY</code> when you also need aggregates. And remember the order of result rows is not promised by either: add <code>ORDER BY</code> whenever the order matters.</p>
<h3>The fan-out trap: grouping after a join</h3>
{co("blue","INTUITION","A join repeats a row once for every partner it matches. An order with 3 item lines appears 3 times after the join. If you now count or sum an <em>order-level</em> fact, you count it 3 times. The group-by was fine; the rows it received were already inflated.")}
{P("3.7.5","(medium) For each customer, count the rows after joining customers, orders and order items, and compare with the true number of orders. Predict for Asha: 4 orders but 7 item lines.")}
{g7}
{fig("ch03d_fanout.png","Bars per customer comparing COUNT star after the join, such as 7 for customer 1, with the true number of orders such as 4","Rows after the join versus the real number of orders for each customer.","the orange bar is what <code>COUNT(*)</code> reports after joining to <code>order_items</code>; the teal bar is the true number of orders. They match only for customers whose every order has exactly one item line (customers 3 and 4). Customer 1 shows 7 against 4 because three of its four orders have two item lines each (2 + 2 + 2 + 1 = 7). See the steps below.")}
{steps([("Step 1","Grain after the join: one row per order line, not per order. Customer 1 has orders 101 (2 lines), 103 (2 lines), 106 (2 lines) and 111 (1 line): 2 + 2 + 2 + 1 = 7 rows."),("Step 2","<code>COUNT(DISTINCT o.order_id)</code> collapses repeats of the order id: 4. That is the right 'number of orders'."),("Step 3","Customer 3 has one order with one line, so both numbers are 1; customer 5 has orders 107 (1 line), 109 (1 line), 113 (2 lines): 4 rows, 3 orders."),("Answer","Use <code>COUNT(DISTINCT order_id)</code> for orders and <code>COUNT(*)</code> only for lines."),("Check","Total real orders: 4 + 3 + 1 + 2 + 3 + 1 = 14. Total rows: 7 + 4 + 1 + 2 + 4 + 2 = 20, the number of lines.")])}
<p><strong>The cleaner cure: aggregate to the right grain first, then join.</strong> Below, a temporary named result <code>order_totals</code> (a CTE, taught in Chapter 5; read it as 'a named mini-table') first collapses lines to one row per order. Joining that to customers cannot multiply anything, because each order now appears once.</p>
{P("3.7.6","(realistic) Paid orders, revenue and average order value per city. First the correct way, then the broken way, and compare the order counts.")}
{g8}
{g8b}
{steps([("Step 1","<code>order_totals</code> has 14 rows, one per order. Joining it keeps the grain at order level, so <code>COUNT(*)</code> really counts orders: Bengaluru 2, Delhi 2, Mumbai 4, Pune 4. Total 12 paid orders."),("Step 2","Revenue per city is the sum of order totals: Bengaluru 760, Delhi 3300, Mumbai 4040, Pune 4560. Total 12660."),("Step 3","AOV = revenue / orders: Bengaluru 380.0, Delhi 1650.0, Mumbai 1010.0, Pune 1140.0."),("Step 4","In the broken query the revenue column is still right (sum of line totals does not double count), but <code>COUNT(*)</code> counts lines: Bengaluru 3 instead of 2, Mumbai 6 instead of 4, Pune 7 instead of 4 (Delhi happens to be unaffected, which is how such bugs hide). Dividing the correct revenue by these wrong counts would give wrong AOVs."),("Check","The correct order counts add to 2 + 2 + 4 + 4 = 12 paid orders. The broken counts add to 3 + 2 + 6 + 7 = 18, which is the number of paid lines, not orders."),("Lesson","The same query can be right for one column and wrong for another. Check every column against a number you can compute independently.")])}
{co("red","COMMON MISTAKE","Joining a detail table (order_items) just to filter or label, then counting rows. Every join to a 'many' side changes the grain. After each join ask: how many result rows per entity now? Cures in order of preference: aggregate before joining; use <code>COUNT(DISTINCT id)</code>; do not join the detail table at all (use <code>EXISTS</code>, Chapter 5).")}
<p><strong>Check yourself.</strong> (1) Which rows form the NULL group? Answer: all rows whose key is NULL, together. (2) A query groups by <code>customer_id</code> and selects <code>name</code>. Safe in PostgreSQL? Answer: no, unless <code>name</code> is also grouped, or customer_id is the table's primary key (PostgreSQL then allows it). (3) What does <code>GROUP BY</code> guarantee about row order? Answer: nothing.</p>
'''
ins("d3",body)

# ---------- 3.8 HAVING in depth ----------
h1=X("""SELECT o.customer_id,
       COUNT(DISTINCT o.order_id)  AS paid_orders,
       SUM(oi.qty * oi.unit_price) AS spent
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY o.customer_id
HAVING COUNT(DISTINCT o.order_id) >= 2
   AND SUM(oi.qty * oi.unit_price) > 1000
ORDER BY spent DESC;""")
h2=X("""SELECT product_id, COUNT(DISTINCT order_id) AS in_orders
FROM order_items
GROUP BY product_id
HAVING COUNT(DISTINCT order_id) >= 4
ORDER BY product_id;""")
h3=X("""SELECT COUNT(*) AS n_orders FROM orders HAVING COUNT(*) > 10;""")
h3b=X("""SELECT COUNT(*) AS n_orders FROM orders HAVING COUNT(*) > 20;""")
h4=X("""SELECT customer_id, COUNT(*) AS n_orders, MIN(status) AS status
FROM orders
GROUP BY customer_id
HAVING MIN(status) = MAX(status)
ORDER BY customer_id;""")
h5=X("""SELECT customer_id,
       COUNT(*) AS orders,
       COUNT(*) FILTER (WHERE status = 'refunded') AS refunded
FROM orders
GROUP BY customer_id
HAVING COUNT(*) FILTER (WHERE status = 'refunded') > 0;""")
h5b=X("""SELECT customer_id, COUNT(*) AS orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) = COUNT(*) FILTER (WHERE status = 'paid')
ORDER BY customer_id;""")
h6=X("""SELECT o.customer_id, SUM(oi.qty * oi.unit_price) AS spent
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY o.customer_id
HAVING SUM(oi.qty * oi.unit_price) >
       (SELECT AVG(s) FROM (SELECT SUM(oi2.qty * oi2.unit_price) AS s
                            FROM orders o2 JOIN order_items oi2 ON oi2.order_id = o2.order_id
                            WHERE o2.status = 'paid'
                            GROUP BY o2.customer_id))
ORDER BY spent DESC;""")
h6b=X("""SELECT AVG(s) AS avg_customer_spend FROM (
  SELECT SUM(oi.qty * oi.unit_price) AS s
  FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
  WHERE o.status = 'paid'
  GROUP BY o.customer_id);""")
h7=X("""SELECT status, COUNT(*) AS n FROM orders WHERE status <> 'paid' GROUP BY status;""")
body=f'''
<h2 id="x8-3-8-having-in-depth">3.8 HAVING in Depth: Filtering Groups Correctly</h2>
<p><code>HAVING</code> is a <code>WHERE</code> for piles. Section 3.3 showed the basics. Here are the shapes you will meet in real work: several conditions, a condition on an aggregate you do not display, a condition on the whole table, a condition that compares a group with all groups, and the 'all rows in the pile satisfy X' pattern.</p>
{fig("ch03d_having.png","Bar chart of paid spend per customer with a dashed line at 1500, bars of customers 1, 2 and 4 green and customers 5 and 6 grey","Paid spend per customer with the HAVING threshold at 1500. Green groups survive, grey groups are removed.","each bar is one customer pile after <code>WHERE status = 'paid'</code> and <code>SUM</code>. The dashed line is the <code>HAVING</code> threshold. A group is kept or dropped as a whole; <code>HAVING</code> never removes single rows from a kept group.")}
{P("3.8.1","(easy) Customers who placed at least 2 paid orders <em>and</em> spent more than 1000 on them. Predict: customer 6 has one paid order of 440; customer 5 has two paid orders but only 760.")}
{h1}
{steps([("Step 1","<code>WHERE</code> keeps paid lines."),("Step 2","Group by customer. Per group compute the number of different orders and the total."),("Step 3","<code>HAVING</code> with <code>AND</code> keeps groups meeting both: customer 1 (4 orders, 4560), 2 (3 orders, 3600) and 4 (2 orders, 3300)."),("Step 4","Customer 5 fails the money test (760), customer 6 fails both."),("Check","Without the money test the first condition alone would keep 1, 2, 4 and 5. Each added condition can only remove groups.")])}
{P("3.8.2","(medium) Products that appear in at least 4 different orders. The count is used only to filter, not displayed. Predict: Notebook is popular; Desk Lamp appears in only 3 orders.")}
{h2}
{steps([("Step 1","<code>COUNT(DISTINCT order_id)</code> per product counts different orders (a product appears once per order because of the primary key, but DISTINCT states the intention)."),("Step 2","<code>HAVING ... &gt;= 4</code> keeps Keyboard (product 1, 4 orders), Mouse (2, 4 orders), Notebook (3, 5 orders) and Pen Pack (4, 4 orders). Desk Lamp (product 5) is in orders 103, 108 and 112 only: 3, so it is dropped."),("Check","Count by hand for the Mouse: orders 102, 106, 111, 114 = 4. The Mug (product 6) has no order lines, so it never forms a group."),("Answer","Products 1, 2, 3 and 4.")])}
{P("3.8.3","(medium) <code>HAVING</code> without <code>GROUP BY</code>: the whole table is one group. Run a 'revenue alert' style test: return the order count only if there are more than 10 orders, then more than 20.")}
{h3}
{h3b}
{steps([("Step 1","With no <code>GROUP BY</code> there is one group, the entire table, so <code>HAVING</code> can keep it or drop it."),("Step 2","14 &gt; 10 is true: the single row survives. 14 &gt; 20 is false: zero rows come back, not a row with 0."),("Meaning","This is a handy health-check shape ('return a row only if something is wrong'), and a reminder that an empty result is different from a result containing 0.")])}
{P("3.8.4","(medium) The 'every row in the pile' pattern. Which customers have all their orders in the same status? Use <code>MIN(x) = MAX(x)</code>. Then find customers with at least one refund, and customers whose orders are <em>all</em> paid.")}
{h4}
{h5}
{h5b}
{steps([("Step 1","If the smallest and largest status in a pile are equal, every value in the pile is that same value. Customers 1, 2, 3, 4 and 6 qualify; customer 5 has paid and refunded, so MIN is paid and MAX is refunded."),("Step 2","'At least one refund' is a count of refunded rows above zero: only customer 5."),("Step 3","'All orders paid' says <code>COUNT(*)</code> equals the count of paid rows. Customer 3 has one cancelled order and customer 5 has a refund, so both fail: 1, 2, 4, 6 remain."),("Answer","Same status: 1, 2, 3, 4, 6. At least one refund: 5. All paid: 1, 2, 4, 6."),("Check","Customer 3 passes the 'same status' test (all cancelled) but not the 'all paid' test, which shows the two questions are different.")])}
{P("3.8.5","(expert-ish) A group compared with all groups: customers whose paid spend is above the average paid spend per customer. Compute that average first, then use it inside <code>HAVING</code>.")}
{h6b}
{h6}
{steps([("Step 1","Inner query: paid spend per customer: 4560, 3600, 3300, 760, 440."),("Step 2","Average of those five: 12660 / 5 = 2532."),("Step 3","<code>HAVING SUM(...) &gt; (subquery)</code> keeps spends above 2532: customers 1, 2 and 4."),("Check","Customers with spend 760 and 440 are below the average. Because the average of a skewed list is pulled up by big spenders, only 3 of 5 customers (60 percent) are above it here."),("Meaning","The subquery returns exactly one number, so it can sit on the right of a comparison. Chapter 5 teaches subqueries properly.")])}
<h3>Pitfalls with row conditions and NULL</h3>
{P("3.8.6","(medium) Count the non-paid orders by status using <code>WHERE status &lt;&gt; 'paid'</code>. What happens to an order whose status is NULL? (The shop has none, but real tables do.)")}
{h7}
{steps([("Step 1","The two non-paid orders are 104 (cancelled) and 109 (refunded)."),("Step 2","<code>status &lt;&gt; 'paid'</code> is unknown when status is NULL, and <code>WHERE</code> keeps only rows where the test is true. So an order with a NULL status would be missing from both <code>= 'paid'</code> and <code>&lt;&gt; 'paid'</code> counts."),("Step 3","If NULL should count as not paid, write <code>WHERE status IS DISTINCT FROM 'paid'</code> (PostgreSQL, SQLite 3.39+) or <code>WHERE status &lt;&gt; 'paid' OR status IS NULL</code>."),("Answer","cancelled 1, refunded 1."),("Meaning","Revisit Chapter 2, Section 2.4: three-valued logic follows you into every aggregate filter.")])}
{co("red","COMMON MISTAKE","Three <code>HAVING</code> errors. (1) Using a <code>SELECT</code> alias in <code>HAVING</code>: <code>HAVING spent &gt; 1500</code> works in SQLite and MySQL but fails in PostgreSQL and SQL Server; repeat the expression. (2) Writing <code>HAVING</code> with a plain column that is not grouped, such as <code>HAVING city = 'Pune'</code> with no <code>GROUP BY city</code>: ambiguous. (3) Expecting <code>HAVING</code> to be fast: it filters after the work of grouping is done, so move every row condition to <code>WHERE</code>.")}
<p><strong>Check yourself.</strong> (1) Can <code>HAVING</code> refer to an aggregate that is not in <code>SELECT</code>? Answer: yes, as in Problem 3.8.2. (2) How do you say 'at least one row in the pile matches'? Answer: <code>HAVING COUNT(*) FILTER (WHERE cond) &gt; 0</code>, or <code>MAX(CASE WHEN cond THEN 1 ELSE 0 END) = 1</code>. (3) What does <code>HAVING COUNT(*) = 0</code> return after <code>GROUP BY</code>? Answer: nothing, since a group has at least one row.</p>
'''
ins("d4",body)
