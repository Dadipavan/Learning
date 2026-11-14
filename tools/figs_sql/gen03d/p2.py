# ---------- 3.6 aggregate functions in depth ----------
rv=X("""CREATE TABLE reviews (reviewer TEXT, score INTEGER);
INSERT INTO reviews VALUES ('A',5),('B',4),('C',NULL),('D',5),('E',3),('F',NULL),('G',4),('H',5);
SELECT COUNT(*)              AS all_rows,
       COUNT(score)          AS answered,
       COUNT(DISTINCT score) AS different_scores,
       SUM(score)            AS total,
       AVG(score)            AS avg_skip_null,
       AVG(COALESCE(score,0)) AS avg_null_as_zero
FROM reviews;""")
cp=X("""SELECT COUNT(*)                AS all_orders,
       COUNT(coupon)           AS with_coupon,
       COUNT(DISTINCT coupon)  AS kinds_of_coupon,
       COUNT(DISTINCT status)  AS kinds_of_status,
       COUNT(DISTINCT customer_id) AS buyers
FROM orders;""")
cat=X("""SELECT p.category,
       COUNT(*)                    AS lines,
       COUNT(DISTINCT oi.order_id) AS orders,
       COUNT(DISTINCT o.customer_id) AS buyers
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders   o ON o.order_id   = oi.order_id
GROUP BY p.category
ORDER BY p.category;""")
em=X("""SELECT COUNT(*) AS n, SUM(qty) AS total_qty, AVG(qty) AS avg_qty,
       MAX(qty) AS max_qty, COALESCE(SUM(qty), 0) AS total_or_zero
FROM order_items
WHERE qty > 1000;""")
tot=X("""SELECT SUM(qty) AS sum_empty, TOTAL(qty) AS total_empty
FROM order_items WHERE qty > 1000;""")
iv=X("""SELECT 7 / 2      AS int_div,
       7 / 2.0    AS dec_div,
       1.0 * 7 / 2 AS forced_dec,
       CAST(7 AS REAL) / 2 AS cast_dec;""")
iv2=X("""SELECT SUM(qty)               AS units,
       COUNT(*)               AS n_lines,
       SUM(qty) / COUNT(*)    AS wrong_int,
       1.0 * SUM(qty) / COUNT(*) AS right_dec,
       AVG(qty)               AS avg_builtin
FROM order_items;""")
sd=X("""SELECT SUM(unit_price)          AS sum_all,
       SUM(DISTINCT unit_price) AS sum_distinct,
       COUNT(DISTINCT unit_price) AS different_prices
FROM order_items;""")
mm=X("""SELECT product_id,
       MIN(qty) AS min_qty, MAX(qty) AS max_qty,
       MAX(qty) - MIN(qty) AS spread
FROM order_items
GROUP BY product_id
ORDER BY product_id;""")
mm2=X("""SELECT MIN(order_date) AS first_order, MAX(order_date) AS last_order,
       MIN(status) AS first_status, MAX(status) AS last_status,
       MIN(coupon) AS min_coupon
FROM orders;""")
gc=X("""SELECT city,
       COUNT(*)              AS n,
       group_concat(name, ', ') AS customers
FROM customers
GROUP BY city
ORDER BY city;""")
ex=X("""SELECT o.customer_id,
       COUNT(DISTINCT o.order_id)  AS n_orders,
       SUM(oi.qty * oi.unit_price) AS spent,
       ROUND(1.0 * SUM(oi.qty * oi.unit_price) / COUNT(DISTINCT o.order_id), 1) AS aov
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY o.customer_id
ORDER BY o.customer_id;""")
aa=X("""SELECT ROUND(AVG(aov), 1) AS avg_of_averages
FROM (SELECT o.customer_id, 1.0 * SUM(oi.qty * oi.unit_price) / COUNT(DISTINCT o.order_id) AS aov
      FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
      WHERE o.status = 'paid'
      GROUP BY o.customer_id);""")
aa2=X("""SELECT ROUND(1.0 * SUM(oi.qty * oi.unit_price) / COUNT(DISTINCT o.order_id), 1) AS true_aov
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid';""")
body=f'''
<h2 id="x6-3-6-aggregate-functions-in-depth">3.6 Aggregate Functions in Depth: COUNT, SUM, AVG, MIN, MAX and String Aggregation</h2>
<p>Section 3.1 listed the functions. Here you learn to <em>choose</em> the right one, to predict the answer with NULL and empty tables in play, and to avoid the five silent errors that produce a believable but wrong number. We climb a ladder: counting first, then sums and averages, then min and max, then joining text together.</p>
<h3>Counting: three functions, three different questions</h3>
{co("green","KEY IDEA","<code>COUNT(*)</code> asks 'how many rows?'. <code>COUNT(col)</code> asks 'in how many rows is <code>col</code> filled in?'. <code>COUNT(DISTINCT col)</code> asks 'how many different filled-in values?'. They only agree when the column has no NULLs and no repeats.")}
{P("3.6.1","(trivial) Eight reviewers gave a score from 1 to 5, but two skipped the question (NULL). Find the number of rows, the number of answers, the number of different scores, the sum, and two averages. Predict first: scores are 5, 4, NULL, 5, 3, NULL, 4, 5.")}
{rv}
{fig("ch03d_nulls.png","Left bars: COUNT(*) 8, COUNT(score) 6, COUNT(DISTINCT score) 3. Right bars: average with NULL skipped 4.33, average with NULL as zero 3.25","Three counts and two averages of the same eight-row column.","on the left the same column gives 8, 6 and 3 depending on the function: eight rows, six answers, three different values (3, 4 and 5). On the right the average is 4.33 if the two blanks mean 'no answer' and 3.25 if they mean 'zero points'. Neither is a database bug; they answer different questions, and you must decide which question is yours.")}
{steps([("Step 1","<code>COUNT(*)</code> counts rows: 8."),("Step 2","<code>COUNT(score)</code> skips the 2 NULLs: 6."),("Step 3","<code>COUNT(DISTINCT score)</code>: the values 5, 4, 3 are the only different ones: 3."),("Step 4","<code>SUM(score)</code> skips NULL: 5 + 4 + 5 + 3 + 4 + 5 = 26."),("Step 5","<code>AVG(score)</code> divides by the 6 real answers: 26 / 6 = 4.3333."),("Step 6","With <code>COALESCE(score,0)</code> the NULLs become 0 and the divisor is 8: 26 / 8 = 3.25."),("Answer","6 answers, 4.33 average among those who answered, 3.25 if non-answers count as zero."),("Meaning","'Average satisfaction of people who responded' is 4.33. A manager who reads 3.25 would think customers are unhappier than they are.")])}
{P("3.6.2","(easy) On the orders table, how many orders have a coupon, how many different coupon codes exist, how many different statuses, and how many different customers placed orders?")}
{cp}
{steps([("Step 1","<code>COUNT(*)</code> = 14 orders, the table size."),("Step 2","<code>COUNT(coupon)</code> counts only non-NULL coupons: the 3 orders 102, 105 and 110."),("Step 3","<code>COUNT(DISTINCT coupon)</code>: all three used the same code SAVE10, so 1 kind."),("Step 4","Statuses are paid, cancelled and refunded: 3 kinds. Customers who ever ordered: 1, 2, 3, 4, 5, 6: 6 buyers."),("Check","The number of orders without a coupon is <code>COUNT(*) - COUNT(coupon)</code> = 14 - 3 = 11, matching Problem 3.P.7.")])}
{P("3.6.3","(realistic) For each product category, how many order lines, how many different orders and how many different customers? Here each number has a different grain, so each needs its own function. Predict: Electronics is bought in many orders, but a customer may buy two electronics items in the same order.")}
{cat}
{steps([("Step 1","Join items to products (for the category) and to orders (for the customer). Now one row is one order line."),("Step 2","<code>COUNT(*)</code> counts lines. <code>COUNT(DISTINCT oi.order_id)</code> counts each order once even if it has two lines of that category. <code>COUNT(DISTINCT o.customer_id)</code> counts each person once."),("Step 3","Read the Electronics row: 8 lines in 7 orders bought by 4 customers (1, 2, 4 and 5). Order 114 contains both a Keyboard and a Mouse, so it contributes 2 lines but 1 order."),("Step 4","Stationery has 9 lines in 7 orders bought by customers 1, 3, 5 and 6. Orders 110 and 113 each contain two stationery products, so lines exceed orders by 2."),("Check","Lines add up to 8 + 3 + 9 = 20, the number of order lines. Orders do <em>not</em> add up to 14 across categories (7 + 3 + 7 = 17), because an order with items from two categories is counted once in each."),("Meaning","'How many customers buy Stationery?' needs <code>COUNT(DISTINCT customer_id)</code>. Using <code>COUNT(*)</code> here would overstate the audience (9 instead of 4).")])}
<p>Look closely at the output above: the lines, orders and buyers columns are different numbers for the same category. Whenever a number must describe a <em>thing</em> (customers, orders), count that thing's key with <code>DISTINCT</code> after a join, or aggregate before joining (Section 3.7).</p>
<h3>SUM and AVG: empty sets, integer division and the DISTINCT trap</h3>
<p>Two special cases surprise people: what <code>SUM</code> returns for no rows at all, and what happens when two integers are divided.</p>
{P("3.6.4","(medium) What do the aggregates return when no row passes the <code>WHERE</code> (here: no order line has more than 1000 units)? Predict first: how many rows does the result have?")}
{em}
{tot}
{steps([("Step 1","An aggregate query without <code>GROUP BY</code> always returns exactly one row, even when the input is empty."),("Step 2","<code>COUNT</code> of nothing is 0, because zero is a perfectly good count."),("Step 3","<code>SUM</code>, <code>AVG</code>, <code>MAX</code> of nothing have no sensible number, so SQL returns NULL."),("Step 4","<code>COALESCE(SUM(qty), 0)</code> converts that NULL to 0 when a report needs a number. SQLite's own <code>TOTAL()</code> does the same but returns a decimal (0.0)."),("Answer","One row: n = 0, the rest NULL (or 0 where you coalesced)."),("Meaning","A dashboard card that shows 'revenue: NULL' on a quiet day is a bug waiting to be reported. Decide whether empty means 0 or 'no data'.")])}
{P("3.6.5","(medium) Integer division. Compute 7 / 2 four ways, then the average units per order line from <code>SUM(qty) / COUNT(*)</code> and from <code>AVG(qty)</code>.")}
{iv}
{iv2}
{steps([("Step 1","Two integers divided with <code>/</code> in SQLite (and in SQL Server, and in PostgreSQL) give an integer: 7 / 2 = 3."),("Step 2","Make either side a decimal and you get 3.5: write <code>7 / 2.0</code>, <code>1.0 * 7 / 2</code> or <code>CAST(7 AS REAL) / 2</code>."),("Step 3","Total units 34 divided by 20 lines: <code>34 / 20</code> as integers is 1 (the 0.7 is thrown away), but the right answer is 1.7."),("Step 4","<code>AVG(qty)</code> already works in decimals in SQLite and gives 1.7."),("Answer","Average units per line is 1.7."),("Check","20 x 1.7 = 34, the total units. Always multiply the average back by the count to see if you get the total.")])}
{co("red","COMMON MISTAKE","Dividing two sums or counts without making one decimal: <code>SUM(qty) / COUNT(*)</code> returns 1 here, not 1.7. MySQL's <code>/</code> always returns a decimal, but PostgreSQL, SQL Server and SQLite truncate integer division, so a query that looks fine on one engine is wrong on another. Habit: write <code>1.0 * SUM(x) / COUNT(*)</code> or use <code>AVG(x)</code>.")}
{P("3.6.6","(medium) The DISTINCT trap. What is the total of <code>unit_price</code> over all order lines, and what does <code>SUM(DISTINCT unit_price)</code> return? Which one is revenue-relevant?")}
{sd}
{steps([("Step 1","<code>SUM(unit_price)</code> adds the price on all 20 lines: 11980. (It is not revenue, since it ignores quantity; it is only a demonstration.)"),("Step 2","<code>SUM(DISTINCT unit_price)</code> first removes repeated prices, leaving 1500, 600, 80, 120, 900, then adds them: 3200."),("Step 3","Five different prices, so <code>COUNT(DISTINCT unit_price)</code> is 5."),("Answer","11980 versus 3200."),("Meaning","Two different lines selling a 600 mouse are two real sales. <code>SUM(DISTINCT amount)</code> counts only one of them and silently under-reports revenue.")])}
{co("red","COMMON MISTAKE","Using <code>SUM(DISTINCT amount)</code> to 'fix' double counting after a join. It removes real sales that merely have the same amount. The safe fixes are to aggregate before joining (Section 3.7) or to sum a per-row key-safe value. <code>DISTINCT</code> belongs with <code>COUNT</code> of an <em>identifier</em>, almost never with <code>SUM</code>.")}
<h3>Average of averages and the weighted average</h3>
<p>An average is a sum divided by a count. If you average two averages you give a group of 1 order the same voice as a group of 100. The correct recipe: add all numerators, add all denominators, divide once.</p>
{P("3.6.7","(realistic) For paid orders compute each customer's average order value, then the plain mean of those averages, and the true average order value (AOV) across all 12 paid orders.")}
{ex}
{aa}
{aa2}
{fig("ch03d_avgavg.png","Bar chart of five customers average paid order value 1140, 1200, 1650, 380, 440 with a dashed line at 962 and a solid line at 1055","Per-customer average order value against the average of averages (962) and the true AOV (1055).","each bar is one customer's own average order value. Customer 4 (two orders) and customer 6 (one order) pull the plain mean of the five bars down to 962, because each customer counts once. The true AOV is 1055 because customer 1 placed four orders and customer 2 three, so their high averages carry more weight in the real total of 12 orders.")}
{steps([("Step 1","Per customer: 4560 / 4 = 1140, 3600 / 3 = 1200, 3300 / 2 = 1650, 760 / 2 = 380, 440 / 1 = 440."),("Step 2","Average of those five: (1140 + 1200 + 1650 + 380 + 440) / 5 = 4810 / 5 = 962."),("Step 3","True AOV: total paid revenue 12660 divided by total paid orders 12 = 1055."),("Answer","962 (wrong) versus 1055 (right) for 'average order value'."),("Check","12 x 1055 = 12660, the real revenue. 12 x 962 = 11544 does not match the revenue, so 962 cannot be the AOV."),("Rule","Never average averages unless every group has the same size. Carry the sum and the count up and divide once.")])}
<h3>MIN and MAX: more than numbers</h3>
{P("3.6.8","(easy) For each product, the smallest and largest quantity ever bought in one line, and the spread (max minus min).")}
{mm}
{steps([("Step 1","Pile order lines by product."),("Step 2","Keyboard (product 1) was always bought one at a time: min = max = 1, spread 0."),("Step 3","Notebook (product 3) ranges from 1 to 5: spread 4. That product has the most variable order size."),("Answer","The table above; the notebook has the largest spread (4).")])}
{P("3.6.9","(medium) <code>MIN</code> and <code>MAX</code> also work on dates and text. Find the first and last order date, the alphabetically first and last status, and the minimum coupon. Predict the coupon: only 3 orders have one.")}
{mm2}
{steps([("Step 1","ISO dates (YYYY-MM-DD) sort the same way as time, so <code>MIN</code> and <code>MAX</code> give the earliest and latest date: 2024-01-10 and 2024-04-20."),("Step 2","Text compares letter by letter: cancelled &lt; paid &lt; refunded."),("Step 3","<code>MIN(coupon)</code> ignores the 11 NULL coupons and returns SAVE10."),("Answer","Dates 2024-01-10 to 2024-04-20, statuses cancelled and refunded, coupon SAVE10."),("Meaning","Dates stored as text work only if they are always in the same sortable format. 'DD-MM-YYYY' text would give nonsense.")])}
<h3>String aggregation: joining the values of a pile into one cell</h3>
<p>Sometimes the pile should become a list, not a number: 'which customers live in each city'. Every database has a function, with a different name.</p>
{tbl(["Database","Function","Example"],[["SQLite, MySQL","<code>group_concat(x, ', ')</code>","<code>group_concat(name, ', ')</code>"],["PostgreSQL, SQL Server 2017+","<code>string_agg(x, ', ')</code>","<code>string_agg(name, ', ' ORDER BY name)</code>"],["Oracle","<code>LISTAGG(x, ', ')</code>","<code>LISTAGG(name, ', ') WITHIN GROUP (ORDER BY name)</code>"],["BigQuery, Snowflake","<code>STRING_AGG</code> / <code>LISTAGG</code>","check the dialect page in Chapter 14"]])}
{P("3.6.10","(medium) List the customers living in each city in one cell, with a count. Predict: Pune has three customers.")}
{gc}
{steps([("Step 1","<code>GROUP BY city</code> makes four piles."),("Step 2","<code>group_concat(name, ', ')</code> glues the names of one pile with a comma and space."),("Step 3","<code>COUNT(*)</code> counts the pile: Pune 3 (Asha, Meena, Tom), Delhi 2, Mumbai 2, Bengaluru 1."),("Answer","The table above."),("Caution","The order of names inside the cell is not guaranteed in SQLite. PostgreSQL lets you write <code>string_agg(name, ', ' ORDER BY name)</code>. Never rely on an unordered list in a report.")])}
<div class="callout green"><div class="lab">REMEMBER</div><div class="txt">Pick the function by the question: rows (<code>COUNT(*)</code>), filled values (<code>COUNT(col)</code>), distinct things (<code>COUNT(DISTINCT id)</code>), total (<code>SUM</code>), typical value among non-NULL (<code>AVG</code>), extremes (<code>MIN</code>/<code>MAX</code>), list (<code>group_concat</code>/<code>string_agg</code>).</div></div>
'''
ins("d2",body)
