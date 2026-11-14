# ---------- 3.10 playbook ----------
k1=X("""SELECT COUNT(*)                                       AS orders,
       COUNT(DISTINCT customer_id)                    AS buyers,
       COUNT(*) FILTER (WHERE status = 'paid')        AS paid_orders,
       ROUND(100.0 * COUNT(coupon) / COUNT(*), 1)     AS pct_orders_with_coupon,
       MIN(order_date)                                AS first_day,
       MAX(order_date)                                AS last_day
FROM orders;""")
k2=X("""SELECT p.name,
       COALESCE(SUM(oi.qty), 0) AS units_sold
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.name
ORDER BY units_sold DESC, p.name;""")
k3=X("""SELECT c.city, COUNT(*) AS paid_orders
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'paid'
GROUP BY c.city
HAVING COUNT(*) >= 3
ORDER BY paid_orders DESC, c.city;""")
k4=X("""SELECT substr(order_date,1,7) AS month,
       COUNT(*) AS paid_orders,
       COUNT(coupon) AS with_coupon,
       ROUND(100.0 * COUNT(coupon) / COUNT(*), 1) AS coupon_pct
FROM orders
WHERE status = 'paid'
GROUP BY month
ORDER BY month;""")
k5a=X("""SELECT p.name, SUM(oi.qty * oi.unit_price) AS revenue
FROM order_items oi JOIN products p ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name
ORDER BY revenue DESC
LIMIT 1;""")
k5b=X("""SELECT p.category, p.name, p.price
FROM products p
JOIN (SELECT category, MAX(price) AS top_price FROM products GROUP BY category) m
  ON m.category = p.category AND m.top_price = p.price
ORDER BY p.category;""")
k5c=X("""SELECT category, name, price FROM (
  SELECT category, name, price,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC, name) AS rn
  FROM products)
WHERE rn = 1
ORDER BY category;""")
k6=X("""CREATE TABLE contacts (id INTEGER, email TEXT);
INSERT INTO contacts VALUES (1,'a@x.com'),(2,'b@x.com'),(3,'a@x.com'),(4,'c@x.com'),(5,'b@x.com'),(6,'a@x.com');
SELECT email, COUNT(*) AS copies, MIN(id) AS keep_id
FROM contacts
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY email;""")
k6b=X("""SELECT COUNT(*) AS rows_total,
       COUNT(DISTINCT email) AS unique_emails,
       COUNT(*) - COUNT(DISTINCT email) AS rows_to_delete
FROM contacts;""")
k7=X("""SELECT p.category,
       COUNT(DISTINCT o.customer_id) AS buyers,
       ROUND(100.0 * COUNT(DISTINCT o.customer_id) /
             (SELECT COUNT(DISTINCT customer_id) FROM orders), 1) AS pct_of_buyers
FROM orders o
JOIN order_items oi ON oi.order_id  = o.order_id
JOIN products    p  ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY buyers DESC, p.category;""")
k8=X("""WITH monthly AS (
  SELECT substr(o.order_date,1,7) AS month, SUM(oi.qty * oi.unit_price) AS revenue
  FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
  WHERE o.status = 'paid'
  GROUP BY month
)
SELECT month, revenue, (SELECT AVG(revenue) FROM monthly) AS avg_month
FROM monthly
WHERE revenue > (SELECT AVG(revenue) FROM monthly)
ORDER BY month;""")
k9=X("""WITH by_product AS (
  SELECT product_id, SUM(qty * unit_price) AS revenue FROM order_items GROUP BY product_id
)
SELECT (SELECT SUM(revenue) FROM by_product)           AS sum_of_groups,
       (SELECT SUM(qty * unit_price) FROM order_items) AS plain_total,
       (SELECT COUNT(*) FROM by_product)               AS n_groups,
       (SELECT COUNT(DISTINCT product_id) FROM order_items) AS n_distinct_keys;""")
k10a=X("""SELECT c.name
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status <> 'paid';""")
k10b=X("""SELECT c.customer_id, c.name,
       COUNT(o.order_id) AS orders,
       COUNT(*) FILTER (WHERE o.status = 'paid') AS paid
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(*) FILTER (WHERE o.status = 'paid') = 0
ORDER BY c.customer_id;""")
body=f'''
<h2 id="x10-3-10-how-to-solve-any-aggregation-group-by-having-and-filter-problem">3.10 How to solve any aggregation, group by, having and filter problem</h2>
<p>Knowing the clauses is not the same as being able to solve a problem you have never seen. This section is a repeatable method. It has five parts: a decision flow, a table that translates words in the question into SQL, eight recurring patterns each with a fully solved example, a way to check any answer, and a way to debug when the answer is wrong or the query will not run.</p>
<h3>Part 1: the decision flow</h3>
{fig("ch03d_flow.png","A flow of eight boxes: say the grain, choose the table, row conditions in WHERE, GROUP BY the key, aggregate with FILTER, conditions on aggregates in HAVING, order and round, check against the plain total","The eight-step decision flow for any grouped query.","start at box 1 and follow the arrows. Boxes 1 and 2 decide <em>what a row of the answer means</em> and which table can supply it. Boxes 3 to 6 follow the same order as the database's own pipeline from Section 3.5. Boxes 7 and 8 are the finish: format, then prove it. If the check in box 8 fails, the red box tells you where to look first.")}
<ol><li><strong>Say the grain out loud.</strong> Finish the sentence 'one row per ___'. If you cannot, you do not yet understand the question. Example: 'revenue by month and category' means one row per month per category.</li><li><strong>Find the table whose rows already have that grain,</strong> or decide which joins you need. For each join to a 'many' side, note that the row count grows (Section 3.7).</li><li><strong>Row conditions go to <code>WHERE</code>:</strong> 'only paid orders', 'in 2024', 'in Pune'. If the condition mentions no count, sum or average, it is a row condition.</li><li><strong><code>GROUP BY</code> the grain key.</strong> If the question has no 'per', 'each' or 'by', there is no GROUP BY: it is a single-row KPI.</li><li><strong>Choose the aggregates,</strong> using <code>FILTER</code> or <code>CASE</code> when one column of the answer needs only some of the rows.</li><li><strong>A condition on an aggregate goes to <code>HAVING</code>:</strong> 'more than 3 orders', 'revenue above average'.</li><li><strong>Order and shape:</strong> <code>ORDER BY</code>, <code>LIMIT</code>, <code>ROUND</code>, readable aliases, <code>NULLIF</code> for divisions.</li><li><strong>Prove it</strong> with the checks in Part 4.</li></ol>
<h3>Part 2: translate the words</h3>
{tbl(["The question says","Think","SQL ingredient"],[
["per, each, by, for every","one pile per value","<code>GROUP BY key</code>"],
["how many orders / rows","count rows of that grain","<code>COUNT(*)</code> or <code>COUNT(DISTINCT order_id)</code> after joins"],
["how many different customers","count unique things","<code>COUNT(DISTINCT customer_id)</code>"],
["total, revenue, units","add up","<code>SUM(...)</code>"],
["average","sum over count; beware weights","<code>AVG</code>, or <code>SUM(x)/COUNT(...)</code> over the right rows"],
["only paid, in 2024, in Pune","a condition on single rows","<code>WHERE</code>"],
["more than 3, at least 2, above 1500 (about a total or count)","a condition on a pile","<code>HAVING</code>"],
["split into, side by side, paid vs refunded columns","several filtered aggregates","<code>FILTER</code> / <code>CASE</code>"],
["rate, share, percent, conversion","one aggregate divided by another","<code>100.0 * a / NULLIF(b, 0)</code>"],
["top, best, highest, most","sort the groups and take some","<code>ORDER BY agg DESC LIMIT n</code> (or join back to the max)"],
["never, none, without, no orders","a count of zero or a missing match","<code>LEFT JOIN</code> + <code>COUNT(right.id) = 0</code>, or <code>NOT EXISTS</code>"],
["duplicates, appears twice","a pile bigger than one","<code>GROUP BY key HAVING COUNT(*) &gt; 1</code>"],
["above the average, compared with all","compare a pile with a number from the whole set","subquery / CTE with the overall aggregate"]])}
<h3>Part 3: the eight recurring patterns, each solved</h3>
<p>Almost every aggregation question in analysis work and interviews is one of the eight shapes below, or a combination of two. For each shape: recognise it, apply the recipe, check the result.</p>
<h3>Pattern 1: the single KPI card (aggregates with no GROUP BY)</h3>
{P("3.10.1","The shop owner wants one row of headline numbers: orders, distinct buyers, paid orders, percent of orders with a coupon, and the first and last order dates.")}
{k1}
{steps([("Recognise","No 'per' in the question: the whole table is one pile. Grain: one row total."),("Recipe","Several aggregates in one <code>SELECT</code>, no <code>GROUP BY</code>. Use <code>FILTER</code> for the paid orders. Use <code>COUNT(DISTINCT ...)</code> for people."),("Compute","14 orders, 6 buyers, 12 paid. Coupons on 3 of 14 orders: 100 * 3 / 14 = 21.4. Dates 2024-01-10 to 2024-04-20."),("Check","12 paid out of 14 is correct against Problem 3.2.1 (12 paid, 1 cancelled, 1 refunded). Percentages lie between 0 and 100.")])}
<h3>Pattern 2: one metric per group, including empty groups</h3>
{P("3.10.2","Units sold for every product, listing products that never sold with 0. Predict: the Mug has no order lines.")}
{k2}
{steps([("Recognise","'For every product' and 'including those never sold': the list of groups comes from the products table, not from order_items."),("Recipe","Start <code>FROM products</code>, <code>LEFT JOIN</code> the detail, group by the product key, and wrap a <code>SUM</code> in <code>COALESCE(..., 0)</code> (or count a right-side column)."),("Compute","Notebook 14, Pen Pack 7, Mouse 5, Keyboard 4, Desk Lamp 4, Mug 0. Total 34."),("Check","34 equals the total units from Problem 3.1.1. Six products in, six rows out: the Mug survived because the join started from products.")])}
<h3>Pattern 3: keep only groups above a threshold (HAVING)</h3>
{P("3.10.3","Which cities have at least 3 paid orders?")}
{k3}
{steps([("Recognise","'At least 3' of something counted per city: a condition on a pile."),("Recipe","<code>WHERE</code> status is paid; group by city; <code>HAVING COUNT(*) &gt;= 3</code>. Here <code>orders</code> is joined only to customers, so one row is one order and <code>COUNT(*)</code> is safe."),("Compute","Mumbai 4 (orders 102, 108, 110, 114) and Pune 4 (101, 103, 106, 111). Delhi has 2 and Bengaluru 2."),("Check","The cities left out total 4 paid orders, and 8 + 4 = 12.")])}
<h3>Pattern 4: rate or share per group</h3>
{P("3.10.4","For each month, the share of paid orders that used a coupon.")}
{k4}
{steps([("Recognise","'Share' = part / whole inside each group."),("Recipe","Numerator <code>COUNT(coupon)</code> (counts only non-NULL coupons), denominator <code>COUNT(*)</code>, multiply by <code>100.0</code> to avoid integer division. Both are over the same filtered rows."),("Compute","January: 2 paid orders, 1 with coupon (102): 50.0. February: 2 paid, 1 coupon (105): 50.0. March: 4 paid, 1 coupon (110): 25.0. April: 4 paid, none: 0.0."),("Check","Total coupons across months: 1 + 1 + 1 + 0 = 3, equal to the 3 coupon orders, all of which are paid.")])}
<h3>Pattern 5: the top group, and the row that holds the maximum</h3>
{P("3.10.5","(a) Which product earns the most revenue? (b) Which product is the dearest in each category? Part (b) is harder: you need the whole row (the name), not just the maximum.")}
{k5a}
{k5b}
{k5c}
{steps([("Recognise (a)","'Top one' by an aggregate: group, aggregate, sort descending, <code>LIMIT 1</code>. Danger: if two groups tie for first, <code>LIMIT 1</code> hides one. Add a tie-breaker in <code>ORDER BY</code> or use <code>RANK</code> (Chapter 8) if ties must all show."),("Recipe (b)","A bare <code>name</code> next to <code>MAX(price)</code> is not portable (Section 3.7). Two safe ways: join back to the per-group maximum (first output), or number the rows within each category with a window function and keep number 1 (second output)."),("Compute","(a) Keyboard, 6000. (b) Electronics: Keyboard 1500; Home: Desk Lamp 900; Stationery: Pen Pack 120."),("Check","Both methods in (b) agree. The join version returns every tied product if two share the maximum; the <code>ROW_NUMBER</code> version returns exactly one per group (name order breaks ties). Pick on purpose.")])}
<h3>Pattern 6: duplicates and uniqueness</h3>
{P("3.10.6","A contacts table has repeated emails. List each email that appears more than once with its number of copies, and say how many rows a de-duplication would delete.")}
{k6}
{k6b}
{steps([("Recognise","'Appears more than once' means a pile with more than one row."),("Recipe","<code>GROUP BY email HAVING COUNT(*) &gt; 1</code>. <code>MIN(id)</code> gives a stable row to keep."),("Compute","a@x.com appears 3 times (ids 1, 3, 6), b@x.com 2 times (2, 5). c@x.com is unique and is not listed. Rows 6; unique emails 3; rows to delete 6 - 3 = 3 (2 copies of a, 1 of b)."),("Check","2 + 1 = 3 extra rows. The identity <code>COUNT(*) - COUNT(DISTINCT key)</code> = number of surplus rows is a one-line duplicate detector.")])}
<h3>Pattern 7: distinct people across a join</h3>
{P("3.10.7","For each category, how many different customers bought it, and what percent of all buyers is that?")}
{k7}
{steps([("Recognise","'How many different customers' after a join to a many-side table: fan-out danger, so <code>COUNT(DISTINCT customer_id)</code>."),("Recipe","Numerator by category; denominator is the number of distinct buyers overall, a scalar subquery (6)."),("Compute","Electronics 4 of 6 = 66.7; Stationery 4 of 6 = 66.7; Home 3 of 6 = 50.0."),("Check","Percentages add to more than 100 (about 183) because a customer can buy from several categories. That is not an error; it tells you the categories overlap.")])}
<h3>Pattern 8: compare a group with the overall average</h3>
{P("3.10.8","Which months had paid revenue above the average month?")}
{k8}
{steps([("Recognise","'Above the average': a pile is compared with a number from all piles."),("Recipe","Compute the monthly totals once in a CTE, then compare each with the average of the CTE."),("Compute","Monthly revenue 2260, 2520, 2980, 4900; average (2260 + 2520 + 2980 + 4900) / 4 = 12660 / 4 = 3165. Only April (4900) is above."),("Check","Three months are below 3165. The big April pulls the average up, so even 2980 is below it. For growth month over month you need <code>LAG</code> (Chapter 8).")])}
<h3>Part 4: how to check an answer</h3>
<p>Run at least three of these checks on every query before you trust it.</p>
<ol><li><strong>Partition check.</strong> Group counts add up to the table count; group sums add up to the plain total (when no filter hides rows).</li><li><strong>Grain check.</strong> Compare <code>COUNT(*)</code> with <code>COUNT(DISTINCT key)</code> on the joined rows. If they differ and you did not expect it, a join multiplied rows.</li><li><strong>Hand-compute one group.</strong> Pick the smallest group, add it up with a pencil from the raw rows, and compare.</li><li><strong>Boundary cases.</strong> What if a group is empty, a value is NULL, two groups tie, the denominator is zero?</li><li><strong>Second method.</strong> Compute the same number a different way (<code>FILTER</code> versus <code>CASE</code>, subquery versus join). Two methods that agree are rarely both wrong.</li><li><strong>Plausibility.</strong> Shares between 0 and 100? Averages between min and max? A count larger than the table is impossible.</li></ol>
{P("3.10.9","Write the partition check for 'revenue per product' as a single query that returns the sum of the groups, the plain total, the number of groups and the number of distinct keys.")}
{k9}
{steps([("Setup","A CTE holds the per-product revenue (the thing you want to verify)."),("Compute","The sum of groups, 14560, equals the plain total 14560, and the group count 5 equals the number of distinct product ids in order_items."),("Answer","Both pairs agree, so no row was lost or counted twice."),("Habit","If the pairs disagree, the first suspect is a join (rows lost by INNER JOIN, rows repeated by one-to-many) or a WHERE that dropped rows.")])}
<h3>Part 5: how to debug when you are stuck</h3>
{tbl(["Symptom","Most likely cause","First test"],[
["Numbers too big, counts larger than the table","fan-out from a one-to-many join","<code>SELECT COUNT(*), COUNT(DISTINCT key)</code> after each join"],
["A group you expected is missing","INNER JOIN or WHERE removed it; or it has no rows","switch to LEFT JOIN from the table that lists the groups; test the WHERE on its own"],
["Zero shows as 1 in a count","<code>COUNT(*)</code> after LEFT JOIN","use <code>COUNT(right.id)</code>"],
["Result NULL where you expected 0","<code>SUM</code>/<code>MAX</code> of an empty or all-NULL pile","wrap in <code>COALESCE</code> or decide NULL is right"],
["Average looks too low","NULLs counted as zero, or <code>ELSE 0</code> in a CASE","compare <code>COUNT(*)</code> with <code>COUNT(col)</code>"],
["Percent is 0 or 100 only","integer division","multiply by <code>100.0</code> first"],
["Error: column must appear in GROUP BY","a plain column neither grouped nor aggregated","add it to GROUP BY or aggregate it"],
["Error: misuse of aggregate","aggregate in WHERE","move that test to HAVING"],
["Totals do not match another report","different filter (cancelled/refunded), time zone, or duplicates","reproduce their filter exactly, then diff by group"],
["Query slow","grouping a huge joined set","filter earlier with WHERE, aggregate before joining, see Chapter 10"]])}
<p>A reliable debugging routine: (1) shrink the problem: filter to one customer or one month where you can verify by hand; (2) remove clauses from the end (<code>HAVING</code>, then <code>GROUP BY</code>) and look at the raw rows; (3) print the row count after each join; (4) add clauses back one at a time.</p>
{P("3.10.10","(debug) A teammate wants customers who never had a paid order and writes <code>LEFT JOIN orders ... WHERE o.status &lt;&gt; 'paid'</code>. Find what is wrong and fix it. The correct answer is Meena (only a cancelled order), Sana and Tom (no orders).")}
{k10a}
{k10b}
{steps([("Symptom","The first query returns Meena and Priya (Priya's refunded order matched the test), but misses Sana and Tom."),("Cause 1","Priya has paid orders too. Row-level <code>WHERE</code> sees her refunded order alone and keeps it. 'Never paid' is a statement about a whole pile, so it needs a group."),("Cause 2","Sana and Tom have NULL status after the LEFT JOIN, and <code>NULL &lt;&gt; 'paid'</code> is unknown, so <code>WHERE</code> drops them."),("Fix","Group by customer and demand a paid count of 0: <code>HAVING COUNT(*) FILTER (WHERE o.status = 'paid') = 0</code>. The filtered count is 0 (not NULL) for customers with no paid rows and for those with no rows at all."),("Answer","Meena (1 order, 0 paid), Sana (0, 0), Tom (0, 0)."),("Lesson","'Never' and 'none' questions are pile questions. A condition on rows cannot say 'no row in the pile satisfies this'.")])}
{co("red","COMMON MISTAKE","Answering a 'never' question with <code>WHERE status &lt;&gt; 'paid'</code>. It finds customers who have <em>some</em> non-paid order, which is a different question. 'No paid order' is: group by customer, count the paid rows, keep groups where that count is 0 (or use <code>NOT EXISTS</code>, Chapter 5).")}
{co("green","KEY IDEA","Method beats memory. Say the grain, put row conditions in WHERE, group by the key, aggregate, put pile conditions in HAVING, then reconcile with a plain total. Eight patterns cover almost everything: KPI card, metric per group, threshold groups, rate per group, top row, duplicates, distinct people, compare with overall.")}
'''
ins("d6",body)
