from _kit import *
db=shop()
X=lambda c: exec_sql(db,c)
st=X("""SELECT 'customers' AS stage, count(*) AS result_rows FROM customers
UNION ALL
SELECT '+ orders', count(*)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
UNION ALL
SELECT '+ order_items', count(*)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
                 LEFT JOIN order_items i ON i.order_id = o.order_id;""")
bad=X("""SELECT c.city, count(*) AS rows_counted, count(DISTINCT c.customer_id) AS real_customers
FROM customers c
LEFT JOIN orders o      ON o.customer_id = c.customer_id
LEFT JOIN order_items i ON i.order_id = o.order_id
GROUP BY c.city ORDER BY c.city;""")
good=X("""SELECT c.city, count(*) AS customers
FROM customers c GROUP BY c.city ORDER BY c.city;""")
body4=f'''
<h2 id="x4-5-seeing-a-join-row-matching-and-row-counts-after-each-join">4.5 Seeing a Join: Row Matching and Row Counts After Each Join</h2>
{co("blue","INTUITION","A join does not <em>merge</em> tables. It creates one output row for every pair of rows that satisfy the <code>ON</code> test. If one customer has four orders, that customer appears four times in the output, and if each order has two items, the customer appears eight times. Once you see joins as 'one output row per matching pair', the duplicate pitfall of Section 4.4 stops being a surprise and becomes arithmetic you can do in your head.")}
{fig("ch04_fanout.png","Left panel shows lines joining each customer to their orders, with Sana unmatched. Right panel shows bars of 8, 16 and 22 rows after successive joins","Left: how a LEFT JOIN matches customers to orders in the shop database. Right: rows in the result after each successive join.","on the left each line is one output row. Asha has four lines, Ravi three, and Sana has none, so she gets one row with NULL order columns. On the right the bars count rows: 8 customers become 16 rows once orders are joined (14 orders plus the 2 customers with no orders), and 22 rows once order items are joined (the 20 item lines plus the same 2 customers). The number of rows grows at every one-to-many step.")}
{P("4.5.1","Count the rows after each join in the chain customers, orders, order items. Predict first: 8 customers; 14 orders plus the 2 customers without orders (Sana and Tom) gives 16; 20 item lines plus those 2 customers gives 22.")}
{st}
{steps([("Step 1","Each stage is the count of the same chain stopped one join earlier. The first is just the customer table, 8 rows."),("Step 2","After joining orders: every order matches its customer, giving 14 rows, plus one row each for the customers with no order. Customers 7 and 8 have none, so 14 + 2 = 16."),("Step 3","After joining items: each order row becomes one row per item line. There are 20 item lines in total, all on real orders, so 20 + 2 unmatched customers = 22."),("Rule","In a chain of <code>LEFT JOIN</code>s the row count equals the count of the most-detailed table that has matches, plus the unmatched rows from above. Compute it before you run the query, and compare.")])}
<p>Now the damage. Ask a seemingly innocent question after the three-table join: how many customers live in each city?</p>
{bad}
{good}
{steps([("Step 1","<code>count(*)</code> after the joins counts <em>result rows</em>, not customers. Pune shows 9, Mumbai 6, Bengaluru 4, Delhi 3, which are the sums of each customer's item lines (or 1 for customers without orders)."),("Step 2","The correct customer counts are in the second result: Pune 3, Mumbai 2, Bengaluru 1, Delhi 2. The first query's <code>count(DISTINCT customer_id)</code> column agrees with them, which is the cheap fix when you must keep the joins."),("Answer","Before aggregating a joined result, ask: what is one row of this result? If it is an order line, then any customer-level number summed over rows is multiplied by the number of lines.")])}
{co("red","COMMON MISTAKE","Using <code>count(*)</code> or <code>sum(customer_level_column)</code> after joining down to a finer grain. The three fixes, best first: (1) aggregate at the right grain in a subquery or CTE <em>before</em> joining, (2) do not join the finer table at all if you do not use its columns, (3) as a last resort use <code>count(DISTINCT key)</code>. A <code>SUM</code> has no <code>DISTINCT</code> fix that is safe, because two different orders can have the same amount and <code>sum(DISTINCT amount)</code> would drop one.")}
<h3>A habit that catches fan-out in ten seconds</h3>
<p>After every join in a long query, add a temporary <code>SELECT count(*), count(DISTINCT &lt;the grain key&gt;)</code>. If the two numbers differ and you did not intend that, a join multiplied rows. Also keep a known total (here, the sum of all paid lines is 12,660) and compare it with the same total computed from your final result.</p>
<h3>Practice with answers</h3>
{qa("4.5.2","Customers (8 rows) <code>LEFT JOIN</code> orders (14 rows, each belonging to one of 6 customers). How many rows does the result have? <em>(easy)</em>","14 matched rows plus 2 customers with no order: 16. The result has at least as many rows as the left table in a <code>LEFT JOIN</code>.")}
{qa("4.5.3","The same customers <code>INNER JOIN</code> orders: how many rows, and which customers vanish? <em>(easy)</em>","14 rows. Sana and Tom (customer ids 7 and 8) disappear because an inner join keeps only pairs that match.")}
{qa("4.5.4","A <code>CROSS JOIN</code> of 8 customers and 6 products returns how many rows, and when is that useful? <em>(medium)</em>","8 x 6 = 48. It is useful for building a complete grid (every customer with every product, then <code>LEFT JOIN</code> actual sales to find the zeros), and dangerous when you forget the <code>ON</code> clause by accident.")}
'''
insert("04","lab4",body4)
fr=X("""CREATE TABLE s (id INTEGER, d INTEGER, v INTEGER);
INSERT INTO s VALUES (1,1,10),(2,2,20),(3,2,30),(4,2,40),(5,4,50),(6,5,60),(7,7,70);
SELECT id, d, v,
  sum(v) OVER (ORDER BY d ROWS   BETWEEN 1 PRECEDING AND CURRENT ROW) AS rows_1,
  sum(v) OVER (ORDER BY d RANGE  BETWEEN 1 PRECEDING AND CURRENT ROW) AS range_1,
  sum(v) OVER (ORDER BY d GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW) AS groups_1,
  sum(v) OVER (ORDER BY d) AS default_frame
FROM s ORDER BY id;""")
body8=f'''
<h2 id="x8-6-frames-in-depth-rows-range-and-groups-with-ties">8.6 Frames in Depth: ROWS, RANGE and GROUPS When Values Tie</h2>
{co("blue","INTUITION","Section 8.4 treated a frame as 'the previous row and this one'. That is true for <code>ROWS</code>, which counts physical rows. But 'one before' can also mean 'one <em>unit of the sort key</em> before' (<code>RANGE</code>) or 'one <em>group of equal keys</em> before' (<code>GROUPS</code>). The three agree when keys are unique and disagree when keys tie or have gaps, which real data always does.")}
<p>Take seven rows sorted by <code>d</code>, where three rows tie at d = 2 and there are gaps (no d = 3, no d = 6). The frame below ends at the current row and starts one step back, measured three different ways:</p>
{P("8.6.1","Compute a two-step sum with <code>ROWS</code>, <code>RANGE</code> and <code>GROUPS</code> frames, and the default frame. Predict first: for row id 5 (d = 4), ROWS adds the previous row, RANGE adds anything with d in [3, 4], GROUPS adds the whole previous group.")}
{fr}
{fig("ch08_frames.png","Three rows of seven boxes showing which rows fall in the frame for row id 5 under ROWS, RANGE and GROUPS","The frame for row id 5 (d = 4) under the three frame types.","each box is a row with its id, sort key d and value v. The orange outline is the current row. Blue boxes are inside the frame. ROWS takes the one physical row before (id 4). RANGE takes rows whose d is within 1 of 4, which is only itself because there is no d = 3. GROUPS takes the whole previous group (the three rows with d = 2) because a group is a set of equal d values.")}
{steps([("Row id 5","<code>rows_1</code> = 40 + 50 = 90. <code>range_1</code>: d between 3 and 4 gives only row 5, so 50. <code>groups_1</code>: the previous group (d = 2) is 20 + 30 + 40 = 90, plus 50 = 140."),("Row id 2","The three rows with d = 2 are peers. <code>range_1</code> and <code>groups_1</code> give all of them 100 (the d = 1 row, plus all three d = 2 rows), but <code>rows_1</code> gives 30, 50, 70, depending on the arbitrary order inside the tie."),("Default frame","With <code>ORDER BY</code> and no frame, SQL uses <code>RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code>. So the running total <code>default_frame</code> gives all three tied rows 100 (10 + 20 + 30 + 40), not 30, 60, 100."),("Answer","Rows are not always the right unit. State the frame explicitly.")])}
{co("red","COMMON MISTAKE","Writing <code>sum(v) OVER (ORDER BY d)</code> for a running total when <code>d</code> has ties. The default frame is <code>RANGE</code>, so tied rows all show the same running total, which jumps by the whole tie group at once. If you want one step per row, add a unique tie-breaker (<code>ORDER BY d, id</code>) <em>or</em> write <code>ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code>. Also, <code>RANGE</code> with a numeric offset (<code>RANGE BETWEEN 1 PRECEDING ...</code>) requires a single numeric or date <code>ORDER BY</code> key. PostgreSQL 11 and later, SQLite 3.28 and later support <code>GROUPS</code>; MySQL and SQL Server do not support <code>GROUPS</code>, and SQL Server limits <code>RANGE</code> to <code>UNBOUNDED</code> and <code>CURRENT ROW</code> boundaries.")}
{qa("8.6.2","A table has daily revenue but some days are missing. You want a 7-day moving average that means 'the last seven <em>calendar days</em>', not 'the last seven rows'. Which frame? <em>(medium)</em>","A date-aware RANGE frame: <code>RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW</code> (PostgreSQL 11+). With missing days a ROWS frame of 6 PRECEDING would reach back further than a week. In engines without interval RANGE, join to a calendar table first so every day exists, then ROWS is correct. Divide by the number of days actually present if gaps remain.")}
{qa("8.6.3","Using the table above, what is <code>sum(v) OVER (ORDER BY d, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)</code> for ids 1 to 7? <em>(what is the output?)</em>","A strict running total in (d, id) order: 10, 30, 60, 100, 150, 210, 280. The unique tie-breaker makes the three d = 2 rows distinct, so the total rises by one row at a time: 30, 60, 100.")}
'''
insert("08","lab8",body8)
