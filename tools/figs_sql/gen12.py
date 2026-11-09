from _kit import *
db=shop()
def X(code): return exec_sql(db, code)
top=X("""WITH rev AS (
  SELECT p.category, p.name, sum(i.qty * i.unit_price) AS revenue
  FROM order_items i
  JOIN orders o   ON o.order_id = i.order_id AND o.status = 'paid'
  JOIN products p ON p.product_id = i.product_id
  GROUP BY p.category, p.name
),
ranked AS (
  SELECT *, row_number() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
  FROM rev
)
SELECT category, name, revenue, rn FROM ranked WHERE rn <= 2 ORDER BY category, rn;""")
fl=X("""CREATE TABLE flights (src TEXT, dst TEXT, hours REAL);
INSERT INTO flights VALUES ('PNQ','BOM',0.5),('BOM','DEL',2),('PNQ','DEL',2.5),
  ('DEL','BLR',2.5),('BOM','BLR',1.7),('BLR','PNQ',1.4),('DEL','BOM',2);""")
route=X("""WITH RECURSIVE route(city, hops, hrs, path) AS (
  SELECT 'PNQ', 0, 0.0, ',PNQ,'
  UNION ALL
  SELECT f.dst, r.hops + 1, r.hrs + f.hours, r.path || f.dst || ','
  FROM route r JOIN flights f ON f.src = r.city
  WHERE r.path NOT LIKE '%,' || f.dst || ',%'   -- cycle guard: never revisit a city
    AND r.hops < 4                               -- depth limit: a second safety net
)
SELECT trim(path, ',') AS path, hops, hrs FROM route WHERE city = 'BLR' ORDER BY hrs LIMIT 3;""")
nog=X("""WITH RECURSIVE route(city, hops) AS (
  SELECT 'PNQ', 0
  UNION ALL
  SELECT f.dst, r.hops + 1 FROM route r JOIN flights f ON f.src = r.city
  WHERE r.hops < 5
)
SELECT count(*) AS rows_without_cycle_guard FROM route;""")
bom=X("""CREATE TABLE bom (parent TEXT, child TEXT, qty INTEGER);
INSERT INTO bom VALUES ('bike','frame',1),('bike','wheel',2),('wheel','rim',1),('wheel','spoke',32),
  ('wheel','tyre',1),('frame','tube',3),('frame','bolt',8),('wheel','bolt',2);
WITH RECURSIVE x(part, need) AS (
  SELECT 'bike', 1
  UNION ALL
  SELECT b.child, x.need * b.qty FROM x JOIN bom b ON b.parent = x.part
)
SELECT part, sum(need) AS total FROM x
WHERE part NOT IN (SELECT parent FROM bom)      -- keep only raw parts (leaves)
GROUP BY part ORDER BY part;""")
lat=X("""CREATE TABLE lat (id INTEGER PRIMARY KEY, ms INTEGER);
INSERT INTO lat (ms) VALUES (12),(15),(11),(250),(14),(16),(13),(18),(12),(900);
WITH s AS (SELECT ms, row_number() OVER (ORDER BY ms) AS rn, count(*) OVER () AS n FROM lat)
SELECT (SELECT avg(ms) FROM lat) AS mean_ms,
       (SELECT avg(ms) FROM s WHERE rn IN ((n + 1) / 2, (n + 2) / 2)) AS median_ms,
       (SELECT min(ms) FROM s WHERE rn >= 0.9 * n) AS p90_ms;""")
iv=X("""CREATE TABLE booking (room TEXT, s TEXT, e TEXT);
INSERT INTO booking VALUES ('A','09:00','10:00'),('A','09:30','11:00'),('A','11:00','12:00'),
  ('A','13:00','14:00'),('A','13:30','13:45'),('B','09:00','09:30');
WITH m AS (
  SELECT *, max(e) OVER (PARTITION BY room ORDER BY s, e
                         ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_end
  FROM booking
),
g AS (
  SELECT *, sum(CASE WHEN prev_end IS NULL OR s > prev_end THEN 1 ELSE 0 END)
            OVER (PARTITION BY room ORDER BY s, e) AS grp
  FROM m
)
SELECT room, min(s) AS start, max(e) AS finish FROM g GROUP BY room, grp ORDER BY room, start;""")
ov=X("""SELECT a.room, a.s, a.e, b.s AS other_s, b.e AS other_e
FROM booking a JOIN booking b
  ON a.room = b.room AND a.rowid < b.rowid AND a.s < b.e AND b.s < a.e;""")
rd=X("""CREATE TABLE visit (day TEXT, uid INTEGER);
INSERT INTO visit VALUES ('d1',1),('d1',2),('d1',1),('d2',2),('d2',3),('d3',1),('d3',3),('d3',4);
WITH f AS (SELECT day, uid, row_number() OVER (PARTITION BY uid ORDER BY day) AS rn FROM visit)
SELECT day,
       count(DISTINCT uid)  AS daily_users,
       sum(rn = 1)          AS new_users,
       sum(sum(rn = 1)) OVER (ORDER BY day) AS cumulative_distinct
FROM f GROUP BY day ORDER BY day;""")
dv=X("""SELECT c.name
FROM customers c
JOIN orders o      ON o.customer_id = c.customer_id AND o.status = 'paid'
JOIN order_items i ON i.order_id = o.order_id
JOIN products p    ON p.product_id = i.product_id AND p.category = 'Electronics'
GROUP BY c.customer_id
HAVING count(DISTINCT p.product_id) = (SELECT count(*) FROM products WHERE category = 'Electronics');""")
body=f'''
<h2 id="x12-7-advanced-pattern-library-top-n-graphs-medians-intervals-and-division">12.7 Advanced Pattern Library: Top-N, Graphs, Medians, Intervals and Division</h2>
{co("blue","INTUITION","Senior analysts do not invent a new query for every question. They recognise a shape: 'best per group', 'path through a network', 'typical value', 'merge overlapping ranges', 'who did all of these'. Each shape has a standard solution. This section is a pattern library: for each shape you get the picture, the query, real output on the shop data or a small table, and the trap.")}
<p>Everything here ran on SQLite 3.50.4 against the shop database from Chapter 2 (or the small tables created in the example). PostgreSQL-only alternatives are shown but marked not run here.</p>
<h3>Pattern 1: top N per group</h3>
{P("12.7.1","Find the two best-selling products by paid revenue in each category. Predict first: Electronics has two products, so both appear; Home has only one sold product; Stationery has two.")}
{top}
{steps([("Step 1","The CTE <code>rev</code> sums paid revenue per product. Cancelled and refunded orders are filtered in the <code>JOIN</code> condition."),("Step 2","<code>row_number() OVER (PARTITION BY category ORDER BY revenue DESC)</code> restarts the count at 1 inside each category."),("Step 3","The outer <code>WHERE rn &lt;= 2</code> keeps the top two. Electronics: Keyboard 4500 (1500 x 3 paid orders), Mouse 3000. Home: Desk Lamp 3600, and Mug never sold, so it has no row. Stationery: Pen Pack 840, Notebook 720."),("Answer","Five rows. A group with fewer than N items returns what it has.")])}
{co("red","COMMON MISTAKE","Using <code>row_number()</code> when ties matter. If two products tie on revenue, <code>row_number()</code> breaks the tie arbitrarily, so a rerun can return a different product. Use <code>rank()</code> or <code>dense_rank()</code> to keep all tied rows (you may then get more than N rows), or add a unique second sort key such as the product id to make the order stable. Also, a window function cannot be used directly in <code>WHERE</code>, which is why the ranking sits in a CTE.")}
<p>PostgreSQL and MySQL 8 also offer <code>CROSS JOIN LATERAL</code>: <code>FROM categories c CROSS JOIN LATERAL (SELECT ... WHERE category = c.category ORDER BY revenue DESC LIMIT 2) t</code> (not run here). It can be faster when you already have a small list of groups and an index on the sort column, because it stops after N rows per group instead of ranking everything.</p>
<h3>Pattern 2: paths through a graph, with cycle protection</h3>
{P("12.7.2","Flights connect cities, and the network has a loop (BLR back to PNQ). Find the three fastest routes from PNQ to BLR. Predict first: the direct-looking route through BOM, 0.5 + 1.7 = 2.2 hours, wins.")}
{fl}
{route}
{steps([("Step 1","The recursive CTE starts at PNQ with an empty route. Each round follows one more flight and adds its hours."),("Step 2","The path is kept as text, <code>,PNQ,BOM,</code>, and the guard <code>NOT LIKE '%,' || dst || ',%'</code> refuses to visit any city already in the path. That is the cycle protection."),("Step 3","The depth limit <code>hops &lt; 4</code> is a second safety net, because one bad row could still make a recursion run for ever."),("Step 4","Filter to arrivals at BLR and sort by hours. Best is PNQ,BOM,BLR at 2.2 hours. Two routes tie at 5.0 hours (PNQ,DEL,BLR is 2.5 + 2.5, PNQ,BOM,DEL,BLR is 0.5 + 2 + 2.5)."),("Answer","A shortest path by total weight, found by listing every acyclic path and sorting. That is fine for small graphs, and a bad idea for large ones (see below).")])}
<p>To see why the guard matters, run the same walk with only a depth limit and no cycle check:</p>
{nog}
<p>With 7 flights and a loop, the walk produced 41 rows by depth 5, because it keeps travelling around the cycle. Without any limit it would never stop (SQLite stops when you press cancel; PostgreSQL runs until memory or time runs out unless you add a limit). PostgreSQL 14 added <code>CYCLE city SET is_cycle USING path</code> to do this bookkeeping for you (not run here).</p>
{co("green","GOING DEEPER","Listing every path grows exponentially with the size of the graph, so this pattern suits hundreds of nodes, not millions. Real shortest-path problems on large graphs belong in a graph database (Chapter 13) or in code (Dijkstra's algorithm). Inside SQL it is still the right tool for hierarchies, which are trees (no cycles), and for 'can I get from A to B in at most 3 steps' questions.")}
<h3>Pattern 3: bill of materials, exploding quantities</h3>
{P("12.7.3","A bike needs 1 frame and 2 wheels. A wheel needs 1 rim, 32 spokes, 1 tyre and 2 bolts. A frame needs 3 tubes and 8 bolts. How many of each raw part for one bike? Predict first: spokes 2 x 32 = 64, bolts 8 + 2 x 2 = 12.")}
{bom}
{steps([("Step 1","Start with 1 bike. Each round joins the BOM and multiplies the quantity needed by the quantity per parent: <code>x.need * b.qty</code>."),("Step 2","A part such as <code>bolt</code> is reached by two routes (via frame: 8, via wheel: 2 wheels x 2 bolts = 4), so it appears twice in the recursion. That is why we <code>sum()</code> at the end."),("Step 3","Keep only leaves: parts that are never a parent. Result: bolt 12, rim 2, spoke 64, tube 3, tyre 2."),("Answer","The multiplication in the recursive step is the whole trick. The same pattern computes org-chart cost roll-ups and recipe ingredient lists.")])}
<h3>Pattern 4: median and percentiles, and why the mean lies</h3>
{P("12.7.4","Ten page-load times in milliseconds contain two slow outliers. Compute the mean, the median and the 90th percentile. Predict first: the mean is dragged far above the typical value by the 900.")}
{lat}
{steps([("Step 1","Sorted: 11, 12, 12, 13, 14, 15, 16, 18, 250, 900. The mean is 1261 / 10 = 126.1."),("Step 2","The median of 10 values is the average of the 5th and 6th: (14 + 15) / 2 = 14.5. The trick <code>rn IN ((n+1)/2, (n+2)/2)</code> picks the one middle row when n is odd and the two middle rows when n is even (integer division)."),("Step 3","The 90th percentile by the nearest-rank method is the value at position 0.9 x 10 = 9, which is 250."),("Answer","The mean says 126 ms, which describes nobody. The median 14.5 ms is the typical user and the p90 of 250 ms is what one user in ten feels. Report medians and percentiles for latency.")])}
<p>PostgreSQL has <code>percentile_cont(0.5) WITHIN GROUP (ORDER BY ms)</code>, which interpolates between neighbours, and <code>percentile_disc</code>, which returns an actual value. SQL Server, Oracle and Snowflake have similar functions. The nearest-rank query above is the portable version. The two methods can give slightly different p90 values, so state which one you use (not run here).</p>
<h3>Pattern 5: merging overlapping intervals</h3>
{P("12.7.5","Room bookings are given as start and end times. Merge overlapping or touching bookings into blocks per room, and also list every pair that overlaps. Predict first: room A has 09:00 to 12:00 (three chained bookings) and 13:00 to 14:00 (13:30 to 13:45 sits inside it).")}
{iv}
{steps([("Step 1","Sort bookings by start inside each room. For each, <code>prev_end</code> is the latest end among all earlier bookings in that room, via <code>max(e)</code> over a frame that stops one row before the current one."),("Step 2","A booking starts a <em>new</em> block when it begins after everything before it has finished (<code>s &gt; prev_end</code>), or when it is the first. The running sum of those flags is a block number: the gaps-and-islands idea from Section 12.5."),("Step 3","Group by block: min start, max end. Room A: 09:00 to 12:00 and 13:00 to 14:00. Room B: 09:00 to 09:30."),("Step 4","The 11:00 booking starts exactly when 09:30-11:00 ends. We used <code>&gt;</code>, so touching bookings merge. Use <code>&gt;=</code> if back-to-back bookings should stay separate."),("Overlap test","Two intervals overlap when <code>a.s &lt; b.e AND b.s &lt; a.e</code>, the one condition to memorise. The pair list below shows the two overlaps, and <code>a.rowid &lt; b.rowid</code> stops each pair appearing twice.")])}
{ov}
{co("red","COMMON MISTAKE","Writing the overlap test as <code>a.s BETWEEN b.s AND b.e</code>. It misses the case where <code>a</code> starts before <code>b</code> and ends after it (a wraps b): neither of a's ends is between b's ends, yet they overlap. Always use the two-inequality form <code>a.s &lt; b.e AND b.s &lt; a.e</code>, which covers every arrangement. PostgreSQL has range types and the <code>&amp;&amp;</code> overlap operator (not run here).")}
<h3>Pattern 6: running distinct count</h3>
{P("12.7.6","Visits by day: how many users per day, how many were seen for the first time that day, and how many distinct users so far? Predict first: day 1 has 2 users, day 2 adds user 3, day 3 adds user 4, so the running total is 2, 3, 4.")}
{rd}
{steps([("Step 1","<code>count(DISTINCT uid)</code> per day works for the daily number, but a window cannot do <code>count(DISTINCT ...) OVER</code> (PostgreSQL and SQLite reject it)."),("Step 2","The workaround: number each user's visits in time order with <code>row_number()</code>. The row with number 1 is the first time that user was ever seen, so <code>sum(rn = 1)</code> counts new users per day."),("Step 3","A running sum of new users is the running distinct count: 2, 3, 4."),("Answer","User 1 appears twice on day 1 (a duplicate event). The daily count is still 2 because of <code>DISTINCT</code>, and only the first of user 1's rows has <code>rn = 1</code> (the other has <code>rn = 2</code>), so user 1 counts once as new.")])}
<h3>Pattern 7: relational division, 'who did all of these'</h3>
{P("12.7.7","Which customers have bought every Electronics product (at least once, paid orders)? Predict first: Electronics has two products (Keyboard and Mouse), so we need customers with both: Asha and Ravi.")}
{dv}
{steps([("Step 1","Restrict to paid orders and to Electronics products with the join conditions."),("Step 2","Group by customer and count <em>distinct</em> products bought. The distinct matters, because buying the keyboard twice is still one product."),("Step 3","Compare to the total number of Electronics products from a subquery, so the query keeps working when the catalogue grows."),("Answer","Asha and Ravi. John bought only the keyboard, so he fails the test.")])}
<p>The same shape answers 'users who completed every onboarding step', 'stores that stock all items on a list', and 'students who passed all required courses'. The pattern: count distinct matches per candidate, compare with the size of the required set.</p>
<h3>Practice with answers</h3>
{qa("12.7.8","Why does the top-N pattern use a CTE or subquery instead of putting <code>rn &lt;= 2</code> in the same query as the window function? <em>(easy)</em>","<code>WHERE</code> runs before window functions are computed, so <code>rn</code> does not exist yet at that stage. The window query goes in a CTE or subquery and the outer query filters it. (PostgreSQL has no <code>QUALIFY</code>, but BigQuery, Snowflake and DuckDB do and it removes the extra layer.)")}
{qa("12.7.9","In the bill of materials, what changes if a part can appear in two different parents at different depths and you forget to <code>sum()</code>? <em>(find the bug)</em>","You would list <code>bolt</code> twice (8 and 4) instead of once as 12, so purchasing would order too few bolts. The recursion correctly produces one row per path, and the final aggregation combines paths.")}
{qa("12.7.10","A table of 500 intervals per user needs the longest single block of continuous activity. Outline the query. <em>(medium)</em>","Merge intervals into blocks as in 12.7.5, then compute <code>max(finish - start)</code> per user over the blocks. In SQL: the grouped result is a CTE, and the outer query takes the maximum duration per user.")}
{qa("12.7.11","Why is a recursive path-listing query risky on a social network with millions of users? <em>(expert)</em>","The number of paths grows exponentially with depth (each person has many friends), so even depth 4 or 5 can create billions of rows, and the cycle guard that tests a growing path string costs more at every step. Use a graph database or an algorithm in code (breadth-first search with a visited set), or limit the depth to 2 or 3 and start from a single person.")}
'''
insert("12","lab12",body)
