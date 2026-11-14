# ---------- 3.9 conditional aggregation in depth ----------
f1=X("""SELECT customer_id,
       COUNT(*) FILTER (WHERE status = 'paid')      AS f_paid,
       COUNT(*) FILTER (WHERE status = 'cancelled') AS f_cancelled,
       COUNT(*) FILTER (WHERE status = 'refunded')  AS f_refunded,
       SUM(CASE WHEN status = 'paid'      THEN 1 ELSE 0 END) AS c_paid,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS c_cancelled,
       SUM(CASE WHEN status = 'refunded'  THEN 1 ELSE 0 END) AS c_refunded
FROM orders
GROUP BY customer_id
ORDER BY customer_id;""")
f2=X("""SELECT COUNT(CASE WHEN status = 'paid' THEN 1 END)        AS count_case_no_else,
       COUNT(CASE WHEN status = 'paid' THEN 1 ELSE 0 END)  AS count_case_else_0_WRONG,
       SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END)    AS sum_case_else_0
FROM orders;""")
f3=X("""WITH order_totals AS (
  SELECT order_id, SUM(qty * unit_price) AS total FROM order_items GROUP BY order_id
)
SELECT o.customer_id,
       ROUND(AVG(CASE WHEN o.status = 'paid' THEN t.total END), 1)         AS aov_paid_only,
       ROUND(AVG(CASE WHEN o.status = 'paid' THEN t.total ELSE 0 END), 1)  AS aov_else_zero
FROM orders o JOIN order_totals t ON t.order_id = o.order_id
WHERE o.customer_id IN (3, 5)
GROUP BY o.customer_id
ORDER BY o.customer_id;""")
f4=X("""SELECT substr(o.order_date,1,7) AS month,
       COALESCE(SUM(oi.qty*oi.unit_price) FILTER (WHERE p.category = 'Electronics'), 0) AS electronics,
       COALESCE(SUM(oi.qty*oi.unit_price) FILTER (WHERE p.category = 'Home'), 0)        AS home,
       COALESCE(SUM(oi.qty*oi.unit_price) FILTER (WHERE p.category = 'Stationery'), 0)  AS stationery,
       SUM(oi.qty*oi.unit_price) AS total
FROM orders o
JOIN order_items oi ON oi.order_id  = o.order_id
JOIN products    p  ON p.product_id = oi.product_id
WHERE o.status = 'paid'
GROUP BY month
ORDER BY month;""")
f4b=X("""SELECT substr(o.order_date,1,7) AS month,
       SUM(oi.qty*oi.unit_price) FILTER (WHERE p.category = 'Home') AS home_raw
FROM orders o
JOIN order_items oi ON oi.order_id  = o.order_id
JOIN products    p  ON p.product_id = oi.product_id
WHERE o.status = 'paid' AND substr(o.order_date,1,7) = '2024-01'
GROUP BY month;""")
f5=X("""SELECT p.category,
       SUM(oi.qty * oi.unit_price) AS revenue,
       ROUND(100.0 * SUM(oi.qty * oi.unit_price) /
             (SELECT SUM(oi2.qty * oi2.unit_price)
              FROM order_items oi2 JOIN orders o2 ON o2.order_id = oi2.order_id
              WHERE o2.status = 'paid'), 1) AS pct_of_paid
FROM orders o
JOIN order_items oi ON oi.order_id  = o.order_id
JOIN products    p  ON p.product_id = oi.product_id
WHERE o.status = 'paid'
GROUP BY p.category
ORDER BY revenue DESC;""")
f6=X("""WITH order_totals AS (
  SELECT order_id, SUM(qty * unit_price) AS total FROM order_items GROUP BY order_id
)
SELECT CASE WHEN t.total <  500  THEN '1 small  (< 500)'
            WHEN t.total <= 1500 THEN '2 medium (500-1500)'
            ELSE                      '3 large  (> 1500)' END AS size_band,
       COUNT(*)       AS n_orders,
       SUM(t.total)   AS revenue
FROM orders o JOIN order_totals t ON t.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY size_band
ORDER BY size_band;""")
f7=X("""SELECT customer_id,
       MIN(order_date) FILTER (WHERE status = 'paid')     AS first_paid,
       MAX(order_date) FILTER (WHERE status = 'refunded') AS last_refund,
       COUNT(*) FILTER (WHERE status = 'refunded')        AS refunds,
       COUNT(*) FILTER (WHERE status = 'cancelled')       AS cancels
FROM orders
GROUP BY customer_id
ORDER BY customer_id;""")
f8=X("""SELECT 1.0 / 0 AS sqlite_div_zero,
       1.0 / NULLIF(0, 0) AS nullif_form;""")
f8b=X("""SELECT customer_id,
       COUNT(*) FILTER (WHERE status = 'refunded')  AS refunds,
       COUNT(*) FILTER (WHERE status = 'cancelled') AS cancels,
       1.0 * COUNT(*) FILTER (WHERE status = 'refunded')
           / NULLIF(COUNT(*) FILTER (WHERE status = 'cancelled'), 0) AS refunds_per_cancel
FROM orders
WHERE customer_id IN (3, 5)
GROUP BY customer_id
ORDER BY customer_id;""")
f9=X("""WITH per_customer AS (
  SELECT c.customer_id, COUNT(o.order_id) AS n_orders
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id
)
SELECT COUNT(*)                                AS signed_up,
       COUNT(*) FILTER (WHERE n_orders >= 1)   AS ordered_once,
       COUNT(*) FILTER (WHERE n_orders >= 2)   AS ordered_twice,
       COUNT(*) FILTER (WHERE n_orders >= 3)   AS ordered_3_plus
FROM per_customer;""")
f9b=X("""WITH per_customer AS (
  SELECT c.customer_id, COUNT(o.order_id) AS n_orders
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id
)
SELECT ROUND(100.0 * COUNT(*) FILTER (WHERE n_orders >= 1) / COUNT(*), 1) AS pct_ordered,
       ROUND(100.0 * COUNT(*) FILTER (WHERE n_orders >= 2)
                   / NULLIF(COUNT(*) FILTER (WHERE n_orders >= 1), 0), 1) AS pct_repeat_of_buyers
FROM per_customer;""")
body=f'''
<h2 id="x9-3-9-filter-and-conditional-aggregation-in-depth">3.9 FILTER and Conditional Aggregation in Depth: Pivots, Rates, Funnels and Buckets</h2>
{co("blue","INTUITION","A plain <code>SUM</code> reads every row of its pile. Conditional aggregation gives each aggregate its own pair of glasses: 'you only see the paid rows', 'you only see the refunded rows'. Several aggregates with different glasses sit side by side in one <code>SELECT</code>, so one pass over the data fills a whole row of a report. That is how you build a pivot table with nothing but <code>GROUP BY</code>.")}
<h3>FILTER and CASE are the same idea</h3>
<ul><li><code>agg(x) FILTER (WHERE cond)</code> is standard SQL (PostgreSQL 9.4+, SQLite 3.30+, DuckDB). It reads like English.</li><li><code>agg(CASE WHEN cond THEN x END)</code> works in every database. Rows failing the condition become NULL, and aggregates skip NULL, so they are ignored. This equivalence is the whole trick.</li><li>MySQL, SQL Server and Oracle have no <code>FILTER</code>: use <code>CASE</code>. BigQuery has <code>COUNTIF</code> and Snowflake <code>COUNT_IF</code> for the counting case. Check your version's documentation.</li></ul>
{P("3.9.1","(easy) For every customer, the number of paid, cancelled and refunded orders, written twice: with <code>FILTER</code> and with <code>CASE</code>. Do they agree? Predict: customer 3 has one cancelled order; customer 5 has two paid and one refunded.")}
{f1}
{steps([("Step 1","One pile per customer (grain: one row per customer)."),("Step 2","Each <code>FILTER (WHERE status = ...)</code> shows only one status to its <code>COUNT</code>."),("Step 3","<code>SUM(CASE WHEN ... THEN 1 ELSE 0 END)</code> adds a 1 for each matching row and a 0 for others, which is also a count."),("Answer","The f_ and c_ columns are identical in every row. Customer 3: 0 paid, 1 cancelled, 0 refunded. Customer 5: 2, 0, 1."),("Check","For every customer the three counts add up to the order count (customer 1: 4 + 0 + 0; customer 5: 2 + 0 + 1 = 3).")])}
<h3>The CASE details that change the answer</h3>
{P("3.9.2","(medium) Three nearly identical expressions, three different meanings: <code>COUNT(CASE WHEN status='paid' THEN 1 END)</code>, <code>COUNT(CASE WHEN status='paid' THEN 1 ELSE 0 END)</code> and <code>SUM(CASE WHEN status='paid' THEN 1 ELSE 0 END)</code>. Which are correct for 'number of paid orders'?")}
{f2}
{steps([("Step 1","Without <code>ELSE</code>, a non-matching row yields NULL, and <code>COUNT</code> skips NULL: only the 12 paid rows are counted."),("Step 2","With <code>ELSE 0</code> inside <code>COUNT</code>, the zero is a real value, not NULL, so every one of the 14 rows is counted. The result is simply <code>COUNT(*)</code> in disguise."),("Step 3","<code>SUM</code> with <code>ELSE 0</code> adds 1 for paid and 0 for the rest: 12."),("Answer","The first and third are correct (12). The second is a bug (14)."),("Rule","Pair <code>COUNT</code> with no <code>ELSE</code> (or <code>ELSE NULL</code>), and <code>SUM</code> with <code>ELSE 0</code>.")])}
{co("red","COMMON MISTAKE","<code>COUNT(CASE WHEN cond THEN 1 ELSE 0 END)</code>. It counts every row because 0 is not NULL. Use <code>COUNT(CASE WHEN cond THEN 1 END)</code>, <code>SUM(CASE WHEN cond THEN 1 ELSE 0 END)</code> or <code>COUNT(*) FILTER (WHERE cond)</code>.")}
{P("3.9.3","(medium) The same <code>ELSE</code> choice changes an <em>average</em>. For customers 3 and 5, compute the average paid-order value two ways: with non-paid orders ignored (no ELSE) and with non-paid orders counted as 0 (ELSE 0). Predict: customer 5 has orders of 360 (paid), 900 (refunded) and 400 (paid).")}
{f3}
{steps([("Step 1","Order totals are needed first, one per order. A CTE (Chapter 5) computes them."),("Step 2","Without ELSE: customer 5 has two paid orders, (360 + 400) / 2 = 380.0. Customer 3 has no paid order, so every CASE value is NULL and <code>AVG</code> of nothing is NULL."),("Step 3","With ELSE 0: customer 5 averages over all three orders, (360 + 0 + 400) / 3 = 253.3. Customer 3 becomes (0) / 1 = 0.0."),("Answer","380.0 versus 253.3 for customer 5; NULL versus 0.0 for customer 3."),("Meaning","'Average paid order value' wants no ELSE. 'Revenue per order placed, counting failures as zero' wants ELSE 0. State which one you mean in a column name.")])}
{co("red","COMMON MISTAKE","Writing <code>AVG(CASE WHEN cond THEN x ELSE 0 END)</code> when you wanted the average of the matching rows only. The zeros enter the denominator and drag the average down. Remove the <code>ELSE</code> to skip non-matching rows.")}
<h3>Pivots: turning values into columns</h3>
{P("3.9.4","(medium) A month-by-category revenue grid of paid orders: one row per month, one column per category, plus a total. Predict: January has no Home sale. What will that cell show without extra care?")}
{f4}
{f4b}
{fig("ch03d_pivot.png","Left a long table with one row per month and category; right stacked bars with one bar per month made of three category colours","Long format (one row per month and category) turned into wide format (one row per month) with FILTER, drawn as stacked bars.","the left side is the output of Problem 3.7.2: many rows, one number each. The right side is the pivoted result: four rows, each month a stacked bar whose three parts are the category columns, and whose total is the printed total column (2260, 2520, 2980, 4900). The pivot does not create information; it rearranges it so a person can read across.")}
{steps([("Step 1","Group by month only: grain is one row per month."),("Step 2","Each category column is <code>SUM(line total) FILTER (WHERE category = ...)</code>, a sum over only that category's lines in the month."),("Step 3","In January there is no Home line, so the filtered <code>SUM</code> sees no rows and returns NULL (the second output shows <code>home_raw</code> = NULL). <code>COALESCE(..., 0)</code> turns it into 0 for the grid."),("Step 4","The unfiltered <code>SUM</code> is the total column."),("Check","In each row the three categories add to the total: Jan 2100 + 0 + 160 = 2260; Feb 1500 + 900 + 120 = 2520; Mar 1200 + 900 + 880 = 2980; Apr 2700 + 1800 + 400 = 4900. The totals add to 12660."),("Meaning","The column list is fixed in the query. A new category needs a new column. For a truly dynamic pivot you need your BI tool or dynamic SQL (Chapter 7).")])}
<h3>Shares, buckets and first/last</h3>
{P("3.9.5","(medium) The share of each category in paid revenue, as a percentage. The denominator is the grand total, a number from a different grain, so we compute it in a scalar subquery.")}
{f5}
{steps([("Step 1","Numerator: paid revenue per category: 7500, 3600, 1560."),("Step 2","Denominator: total paid revenue 12660, computed once by the subquery (it has no <code>GROUP BY</code>, so it returns one number)."),("Step 3","<code>100.0 * 7500 / 12660 = 59.2</code>; <code>100.0 * 3600 / 12660 = 28.4</code>; <code>100.0 * 1560 / 12660 = 12.3</code>."),("Check","59.2 + 28.4 + 12.3 = 99.9: the shares add to 100 only up to rounding. Always say 'rounded'."),("Meaning","Electronics makes about 59 percent of paid revenue. A share is a ratio of an aggregate at one grain to an aggregate at a coarser grain; Chapter 8 shows <code>SUM() OVER ()</code> as a neater way to get that denominator.")])}
{P("3.9.6","(medium) <code>CASE</code> as a grouping key (bucketing). Bucket paid orders by size: small under 500, medium 500 to 1500, large above 1500, with order counts and revenue.")}
{f6}
{steps([("Step 1","Order totals of paid orders: 1660, 600, 1020, 1500, 1280, 360, 900, 440, 600, 1800, 400, 2100."),("Step 2","The <code>CASE</code> turns each total into a label. Small (&lt; 500): 360, 440, 400 = 3 orders, revenue 1200. Medium (500 to 1500): 600, 1020, 1500, 1280, 900, 600 = 6 orders, revenue 5900. Large (&gt; 1500): 1660, 1800, 2100 = 3 orders, revenue 5560."),("Step 3","<code>GROUP BY size_band</code> groups by the label."),("Check","3 + 6 + 3 = 12 paid orders; 1200 + 5900 + 5560 = 12660 revenue."),("Meaning","Only 3 of 12 orders are large, but they bring 44 percent of revenue (5560 / 12660). Bucketing is how histograms and segmentation are made in SQL.")])}
{P("3.9.7","(medium) First paid order, last refund, counts of refunds and cancellations per customer in one row. Predict: most customers have no refund, so <code>MAX</code> of nothing is NULL.")}
{f7}
{steps([("Step 1","Each aggregate gets its own filter, so one group scan yields all four columns."),("Step 2","<code>MIN(order_date)</code> over only paid rows is the first purchase date. Customer 3 has no paid order: NULL."),("Step 3","Only customer 5 has a refund (2024-03-25). Everyone else has NULL there."),("Answer","The table above. NULL means 'no such rows', which is different from 0 in a count column."),("Check","Both count columns are consistent with Problem 3.9.1.")])}
<h3>Rates, ratios and the divide-by-zero guard</h3>
{P("3.9.8","(medium) What happens with division by zero? SQLite returns NULL; PostgreSQL and SQL Server raise an error. Write a portable ratio of refunds per cancellation for customers 3 and 5.")}
{f8}
{f8b}
{steps([("Step 1","Customer 3 has 0 refunds and 1 cancellation: ratio 0.0 / 1 = 0.0."),("Step 2","Customer 5 has 1 refund and 0 cancellations. Dividing by 0 would be an error in PostgreSQL."),("Step 3","<code>NULLIF(x, 0)</code> returns NULL when x equals 0, otherwise x. Dividing by NULL gives NULL (unknown), never an error."),("Answer","Customer 3: 0.0; customer 5: NULL (undefined, not infinity and not 0)."),("Meaning","Reports should show 'n/a' for undefined ratios, not fake zeros that average into other numbers.")])}
{P("3.9.9","(realistic) A funnel. Of the 8 customers who signed up, how many ordered at least once, at least twice and at least three times? Then the conversion percentages. Predict: customers 7 and 8 never ordered.")}
{f9}
{f9b}
{steps([("Step 1","Inner query: one row per customer with their order count. <code>LEFT JOIN</code> keeps customers 7 and 8 with 0 (the <code>COUNT(o.order_id)</code> trick from Problem 3.7.1)."),("Step 2","Outer query: one pile (no GROUP BY) with four counts, each seeing a different subset."),("Step 3","Orders per customer are 4, 3, 1, 2, 3, 1, 0, 0. At least one: 6. At least two: 4 (customers 1, 2, 4, 5). At least three: 3 (customers 1, 2, 5)."),("Step 4","6 / 8 = 75.0 percent ordered. Repeat buyers as a share of buyers: 4 / 6 = 66.7 percent."),("Check","The counts never increase down the funnel: 8, 6, 4, 3."),("Meaning","Choose the denominator on purpose: 'of all sign-ups' (50 percent repeat) or 'of buyers' (66.7). Different denominators give different headlines; write which one you used.")])}
{co("red","COMMON MISTAKE","Forgetting that a filtered <code>SUM</code> with no matching rows is NULL, not 0, and that NULL added to a number gives NULL: <code>jan_home + jan_stationery</code> would be NULL in the pivot. Wrap each filtered sum in <code>COALESCE(..., 0)</code> if you add them, or use the unfiltered total column.")}
<p><strong>Check yourself.</strong> (1) Rewrite <code>SUM(x) FILTER (WHERE y &gt; 3)</code> without FILTER. Answer: <code>SUM(CASE WHEN y &gt; 3 THEN x END)</code>. (2) What does <code>AVG(CASE WHEN c THEN x ELSE 0 END)</code> compute? Answer: the average over all rows with non-matching rows counted as zero. (3) How many columns can a pivot have? Answer: as many as you write; the list is fixed in the SQL text.</p>
'''
ins("d5",body)
