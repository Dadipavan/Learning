from _kit import *
SETUP='''import sqlite3, random
random.seed(7)
db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE big (id INTEGER PRIMARY KEY, customer_id INT, created TEXT, email TEXT, amount INT)")
rows = [(i, random.randint(1, 2000), "2024-%02d-%02d" % (random.randint(1, 12), random.randint(1, 28)),
         "user%d@Mail.com" % i, random.randint(10, 999)) for i in range(1, 50001)]
db.executemany("INSERT INTO big VALUES (?,?,?,?,?)", rows)

def cost(q, args=()):
    """count SQLite virtual-machine steps: a stable stand-in for 'work done'"""
    n = [0]
    def tick():
        n[0] += 1
        return 0
    db.set_progress_handler(tick, 1)
    db.execute(q, args).fetchall()
    db.set_progress_handler(None, 0)
    return n[0]

def plan(q):
    return db.execute("EXPLAIN QUERY PLAN " + q).fetchall()[0][3]
'''
b1=SETUP+'''
tests = [
  ("function on column", "SELECT count(*) FROM big WHERE substr(created, 1, 7) = '2024-03'",
                         "SELECT count(*) FROM big WHERE created >= '2024-03-01' AND created < '2024-04-01'", None),
  ("lower() on column",  "SELECT count(*) FROM big WHERE lower(email) = 'user77@mail.com'",
                         "SELECT count(*) FROM big WHERE lower(email) = 'user77@mail.com'",
                         "CREATE INDEX i_lemail ON big(lower(email))"),
  ("arithmetic on column", "SELECT count(*) FROM big WHERE customer_id + 1 = 43",
                         "SELECT count(*) FROM big WHERE customer_id = 42", None),
]
db.execute("CREATE INDEX i_created ON big(created)")
db.execute("CREATE INDEX i_cust ON big(customer_id)")
for name, bad, good, new_index in tests:
    print(name)
    print("  slow :", cost(bad), "steps |", plan(bad))
    if new_index:
        db.execute(new_index)
        print("  (created the expression index)")
    print("  fast :", cost(good), "steps |", plan(good))
'''
b1out=pyrun(b1)
b2=SETUP+'''
db.execute("CREATE INDEX i_ci ON big(created, id)")
for page in (1, 100, 500):
    off = (page - 1) * 20
    a = cost("SELECT id, created FROM big ORDER BY created, id LIMIT 20 OFFSET ?", (off,))
    last = db.execute("SELECT created, id FROM big ORDER BY created, id LIMIT 1 OFFSET ?", (max(off - 1, 0),)).fetchone()
    k = cost("SELECT id, created FROM big WHERE (created, id) > (?, ?) ORDER BY created, id LIMIT 20", last)
    print("page %3d  OFFSET: %6d steps   keyset: %5d steps" % (page, a, k))
'''
b3='''import sqlite3
db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE ev (id INTEGER PRIMARY KEY, status TEXT, v INT)")
db.executemany("INSERT INTO ev VALUES (?,?,?)", [(i, 'done' if i % 100 else 'failed', i) for i in range(1, 50001)])
db.execute("CREATE INDEX i_status ON ev(status)")

def run(label):
    for st in ("done", "failed"):
        q = "SELECT count(*), sum(v) FROM ev WHERE status = '%s'" % st
        n = [0]
        def tick():
            n[0] += 1
            return 0
        db.set_progress_handler(tick, 1)
        db.execute(q).fetchall()
        db.set_progress_handler(None, 0)
        p = db.execute("EXPLAIN QUERY PLAN " + q).fetchall()[0][3]
        print(label, st.ljust(6), str(n[0]).rjust(7), "steps |", p)

run("before ANALYZE:")
db.execute("ANALYZE")
print(db.execute("SELECT tbl, idx, stat FROM sqlite_stat1").fetchall())
run("after  ANALYZE:")
'''
body = f'''
<h2 id="x10-5-performance-lab-sargability-pagination-and-statistics">10.5 Performance Lab: Sargability, Pagination and Statistics You Can Measure</h2>
{co("blue","INTUITION","A phone book is sorted by surname. Finding 'Rao' takes seconds because you can jump. Finding everyone whose surname, <em>spelled backwards</em>, starts with 'oa' takes hours, because the sorting no longer helps and you must read every line. A query is <strong>sargable</strong> (Search ARGument ABLE) when its <code>WHERE</code> test is written so that an index can jump. This section makes you measure the difference instead of trusting it.")}
<p>To measure work without depending on a fast or slow laptop, the lab counts <strong>SQLite virtual-machine steps</strong>: every query is compiled into small instructions, and we count how many run. Fewer steps means less work. The exact counts depend on your SQLite version (this run used 3.50.4), so compare the ratios, not the digits. PostgreSQL shows the same ideas through <code>EXPLAIN ANALYZE</code> (not run here).</p>
<h3>Sargability: five rewrites that decide whether an index is used</h3>
<p>The rule: an index stores the <em>column value</em>, so the test must compare the bare column with something. Wrap the column in a function or arithmetic and the database cannot use the sorted order.</p>
{tbl(["Slow form (index ignored)","Fast form (index usable)","Why"],[
["<code>WHERE substr(created,1,7) = '2024-03'</code>","<code>WHERE created &gt;= '2024-03-01' AND created &lt; '2024-04-01'</code>","a date range is a contiguous slice of the sorted index"],
["<code>WHERE lower(email) = 'a@x.com'</code>","expression index on <code>lower(email)</code>, same query","the index stores exactly what the query compares"],
["<code>WHERE customer_id + 1 = 43</code>","<code>WHERE customer_id = 42</code>","move arithmetic to the constant side"],
["<code>WHERE name LIKE '%son'</code>","<code>WHERE name LIKE 'son%'</code>, or a trigram index (PostgreSQL <code>pg_trgm</code>)","a B-tree can only follow a known prefix"],
["<code>WHERE a = 1 OR b = 2</code>","<code>UNION ALL</code> of two queries, or one index on each column (PostgreSQL combines them with a bitmap OR)","a single B-tree cannot answer two different columns at once"]])}
{P("10.5.1","Run the first three rewrites on a 50,000-row table and compare steps. Predict first: the slow forms touch all 50,000 rows (about 200,000 steps, four per row), the fast forms touch a small slice.")}
{pyblock(b1)}
{steps([("Step 1","The first pair filters by month. <code>substr(created,1,7)</code> is a function of the column, so the plan says <code>SCAN</code> and every row is read. The range form says <code>SEARCH ... (created&gt;? AND created&lt;?)</code>: the index jumps to 2024-03-01 and stops at 2024-04-01. Steps fall from 204,116 to 12,322, about 17 times fewer."),
("Step 2","The second pair uses the same query text. The only change is the new expression index on <code>lower(email)</code>, which stores the lowercase value. The scan (200,013 steps) becomes a search (18 steps). You changed the index, not the query."),
("Step 3","The third pair moves <code>+ 1</code> to the other side of the equals sign: 200,030 steps become 64."),
("Answer","Keep the column bare on one side of the comparison. If you cannot, index the expression.")])}
{co("red","COMMON MISTAKE","Writing a date filter as <code>WHERE DATE(created_at) = '2024-03-15'</code> or <code>WHERE EXTRACT(YEAR FROM created_at) = 2024</code> on a large table. It works and returns correct rows, so nothing warns you, yet it reads every row. Right: <code>WHERE created_at &gt;= '2024-03-15' AND created_at &lt; '2024-03-16'</code>. A second trap is a type mismatch, such as comparing a text column to a number (<code>WHERE phone = 5551234</code>): the database may convert every stored value and skip the index.")}
{P("10.5.2","(find the slow part) A teammate reports that <code>SELECT * FROM big WHERE amount * 1.1 &gt; 500</code> is slow even though <code>amount</code> is indexed. Fix it. Predict first: the multiplication is on the column side.")}
{steps([("Idea","Divide the constant instead: <code>amount * 1.1 &gt; 500</code> is the same as <code>amount &gt; 500 / 1.1</code>."),("Rewrite","<code>WHERE amount &gt; 454.55</code> (500 / 1.1 = 454.545..., so use 454.55 for integers: <code>amount &gt;= 455</code> because 455 x 1.1 = 500.5 is above 500 and 454 x 1.1 = 499.4 is not)."),("Check","Integer amounts 455 and up pass the original test, 454 and below fail. Both forms return the same rows, and the second can use an index on <code>amount</code>.")])}
<h3>Pagination: OFFSET gets slower with every page, keyset does not</h3>
<p>A web page shows 20 rows at a time. The obvious query is <code>ORDER BY created, id LIMIT 20 OFFSET 9980</code>. The database cannot skip 9,980 rows without walking past them, so page 500 costs 500 times what page 1 costs. <strong>Keyset pagination</strong> (also called the seek method) remembers the last row of the previous page and asks for rows after it, so the index jumps straight there.</p>
{P("10.5.3","Fetch page 1, page 100 and page 500 both ways. Predict first: OFFSET cost grows in proportion to the page number, keyset cost stays about the same.")}
{pyblock(b2)}
{steps([("Step 1","OFFSET steps grow by about 4,000 per 100 pages: 130, 4,090, 20,090. That is 200 steps per page of skipped rows."),("Step 2","The keyset form uses <code>WHERE (created, id) &gt; (last_created, last_id)</code>, a row-value comparison that the index on <code>(created, id)</code> answers by seeking. Its cost stays under about 1,400 steps whatever the page (it is not perfectly flat here because many rows share one date). On page 1 it is slightly more expensive, since there is no previous row to seek from."),("Answer","Use keyset for feeds and infinite scroll. Keep OFFSET for small tables or when users must jump to page 37.")])}
{fig("ch10_pagination.png","Line chart of SQLite virtual machine steps against page number, OFFSET rising linearly and keyset staying low","Work needed to fetch one page of 20 rows from a 50,000-row table, measured on SQLite 3.50.4.","the orange line is OFFSET paging: it climbs in a straight line because each deeper page skips more rows. The blue line is keyset paging: it wobbles but never climbs. The vertical gap at page 500 is the price of skipping 9,980 rows.")}
{co("red","COMMON MISTAKE","Keyset pagination on a column that is not unique. If you page by <code>created</code> alone and ten rows share one timestamp, rows can be skipped or repeated at the page boundary. Always add a unique tie-breaker (<code>created, id</code>) to both the <code>ORDER BY</code> and the <code>WHERE</code>. Also, row-value comparison <code>(a, b) &gt; (x, y)</code> works in PostgreSQL, MySQL and SQLite but not in SQL Server, where you write <code>a &gt; x OR (a = x AND b &gt; y)</code>.")}
<h3>Statistics: why the planner sometimes guesses wrong</h3>
<p>Before running a query the planner estimates how many rows each step returns, using <strong>statistics</strong> collected by <code>ANALYZE</code>. If the estimate is far from reality, it picks a bad plan: it scans when it should seek, or the other way round. The classic cause is <strong>skew</strong>: 99 percent of rows share one value, and statistics that only keep an average cannot see that.</p>
{P("10.5.4","A table has 50,000 events, 99 percent with status <code>done</code> and 1 percent <code>failed</code>, with an index on <code>status</code>. Compare the plans for both values before and after <code>ANALYZE</code>. Predict first: both look the same to a planner that only knows the average.")}
{pyblock(b3)}
{steps([("Step 1","Before <code>ANALYZE</code> SQLite has no statistics and uses the index for both values. For <code>failed</code> (500 rows) that is right: 3,013 steps. For <code>done</code> (49,500 rows) it is wasteful, 297,014 steps, because it hops from index to table 49,500 times."),("Step 2","<code>ANALYZE</code> stores <code>'50000 25000'</code>: 50,000 rows, on average 25,000 rows per status value. Two values, so the average is exactly half the table."),("Step 3","With that average the planner decides an index is not worth it and scans for <em>both</em>. That helps <code>done</code> slightly (298,513 steps, about the same) but makes <code>failed</code> 50 times worse (151,513 vs 3,013)."),("Answer","Statistics are summaries, and summaries hide skew. PostgreSQL keeps a list of most common values and a histogram, so it knows that <code>failed</code> is rare; SQLite builds with STAT4 do something similar. Always compare estimated and actual row counts in <code>EXPLAIN ANALYZE</code> (not run here); a 10x gap is your signal.")])}
{co("green","GOING DEEPER","PostgreSQL fixes a bad estimate in this order: (1) run <code>ANALYZE table</code> because statistics may simply be old, (2) raise the detail with <code>ALTER TABLE t ALTER COLUMN c SET STATISTICS 1000</code>, (3) add extended statistics for correlated columns (<code>CREATE STATISTICS s (dependencies) ON city, zip FROM t</code>), because the planner multiplies the selectivities of two columns as if they were independent, and city and zip are not, (4) as a last resort rewrite the query. The <em>autovacuum</em> daemon runs <code>ANALYZE</code> automatically, but after a bulk load you should run it yourself. None of these commands were run here.")}
<h2 id="x10-6-index-types-join-algorithms-and-partitioning">10.6 Index Types, Join Algorithms and Partitioning</h2>
{co("blue","INTUITION","So far an index meant a B-tree: a sorted tree. Think of it as the index at the back of a textbook, sorted alphabetically. Other books need other indexes: a map index (find everything near this place), a keyword index for chapters that mention several words, a table of contents that only says which <em>block of pages</em> to look in. PostgreSQL offers each of these as an index type.")}
{fig("ch10_btree.png","Diagram of a B-tree with a root, three branch nodes and four linked leaf pages, with a lookup of key 44 highlighted","A B-tree lookup of key 44 in a tiny tree: root, branch, leaf.","start at the root and follow the arrow whose range contains 44 (between 30 and 60). The branch sends you between 40 and 50, and the leaf holds 44 with a pointer to the table row. That is three page reads. A real tree holds hundreds of keys per page, so even a billion-row table is only four or five levels deep. The dotted arrows between leaves are why range queries (<code>BETWEEN</code>, <code>ORDER BY</code>) are fast: after finding the start, walk sideways.")}
<h3>Index types at a glance (PostgreSQL, not run here)</h3>
{tbl(["Type","Best for","Does not help with"],[
["B-tree (default)","equality, ranges, <code>ORDER BY</code>, prefix <code>LIKE 'abc%'</code>","searching inside arrays or text, or the last letters of a string"],
["Hash","equality only, small and fast keys","ranges, sorting (rarely better than B-tree)"],
["GIN","many values per row: arrays, <code>jsonb</code>, full-text search, trigrams","range sorting; writes are slower"],
["GiST","geometry, nearest-neighbour, ranges overlap (<code>&amp;&amp;</code>), exclusion constraints","exact equality on plain numbers"],
["BRIN","huge tables whose physical order follows the column (logs by timestamp); the index is tiny","randomly ordered columns"],
["Partial / expression","only some rows, or a computed value (Section 10.2)","queries that do not repeat the same condition"]])}
{P("10.6.1","Pick the index for each: (a) <code>WHERE tags @&gt; ARRAY['sale']</code> on a text-array column, (b) 2 billion sensor rows appended in time order, queried by time window, (c) <code>WHERE email = ?</code>, (d) find the 10 nearest shops to a point. Predict first: four different answers.")}
{steps([("(a)","GIN: it stores one entry per array element, so containment search is direct."),("(b)","BRIN: it stores the min and max timestamp per block of pages, a few megabytes for terabytes of data. It only works because rows arrive in time order."),("(c)","B-tree (hash would work for pure equality, but B-tree is the safe default and supports uniqueness)."),("(d)","GiST (or SP-GiST): it supports distance ordering with <code>ORDER BY location &lt;-&gt; point LIMIT 10</code>.")])}
<h3>Join algorithms, measured</h3>
<p>Section 10.3 listed the three join algorithms. SQLite uses nested loops, so we can measure one. We join 2,000 customers to 50,000 orders and keep customers 1 to 50:</p>
{pyblock(SETUP.split("def cost")[0].replace('db.execute("CREATE TABLE big','db.execute("CREATE TABLE cust (customer_id INTEGER PRIMARY KEY, name TEXT)")\ndb.executemany("INSERT INTO cust VALUES (?,?)", [(i, "c%d" % i) for i in range(1, 2001)])\ndb.execute("CREATE TABLE big')+'''
def cost(q):
    n = [0]
    def tick():
        n[0] += 1
        return 0
    db.set_progress_handler(tick, 1)
    db.execute(q).fetchall()
    db.set_progress_handler(None, 0)
    return n[0]

q = "SELECT count(*) FROM cust c JOIN big b ON b.customer_id = c.customer_id WHERE c.customer_id <= 50"
def plans(q):
    return " ; ".join(r[3] for r in db.execute("EXPLAIN QUERY PLAN " + q).fetchall())
print("no index   :", cost(q), "steps |", plans(q))
db.execute("CREATE INDEX i_cust ON big(customer_id)")
print("with index :", cost(q), "steps |", plans(q))
''')}
{steps([("Step 1","Without an index on <code>big.customer_id</code> the plan reads: <code>SCAN b</code> (all 50,000 orders, outer loop) then <code>SEARCH c</code> by primary key for each one. SQLite picked the big table as the outer loop because that is the cheapest order it could find. Cost: 251,242 steps."),("Step 2","With the index, the plan flips: <code>SEARCH b USING COVERING INDEX i_cust (customer_id&lt;?)</code> reads only the orders of customers 1 to 50, then looks each customer up. Cost: 8,613 steps, about 29 times less."),("Step 3","Notice that the planner also chose a different join <em>order</em>. Join order is part of the plan and it changes when indexes change."),("Answer","A nested loop is fast exactly when the inner side can be probed with an index (here the primary key of <code>c</code>). A hash join (PostgreSQL) instead builds a hash table of the smaller input once and probes it, which is why it wins for big unindexed equality joins. A merge join wins when both inputs already arrive sorted. You rarely choose the algorithm; you make the right index or statistics exist and read the plan.")])}
<h3>Partitioning: splitting one big table into many</h3>
<p><strong>Partitioning</strong> splits a table into physical pieces by a rule, usually a date range, while queries still address one table name. The pay-off is <strong>partition pruning</strong>: when the <code>WHERE</code> clause fixes the date, the planner skips whole pieces. A second pay-off is housekeeping: dropping an old month is <code>DROP TABLE orders_2023_01</code>, instant, instead of a huge <code>DELETE</code> that leaves dead rows.</p>
{sql("""-- PostgreSQL (not run here)
CREATE TABLE orders (
  order_id   bigint,
  order_date date NOT NULL,
  amount     numeric
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2024_03 PARTITION OF orders
  FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');
CREATE TABLE orders_2024_04 PARTITION OF orders
  FOR VALUES FROM ('2024-04-01') TO ('2024-05-01');

-- retire old data without a giant DELETE
ALTER TABLE orders DETACH PARTITION orders_2024_03;""")}
{fig("ch10_partition.png","Six monthly partitions of an orders table with only the March partition highlighted as read","Partition pruning for a query that filters on March 2024.","the filter at the top matches only the March box, so only that partition is opened. The other five are proven irrelevant from their boundaries, which is why <code>EXPLAIN</code> lists a single partition. If the filter did not mention <code>order_date</code>, every box would be read.")}
{co("red","COMMON MISTAKE","Partitioning a table of 5 million rows 'for speed'. Partitioning helps when the table is large (hundreds of millions of rows, or too big to maintain) <em>and</em> most queries filter on the partition key. Otherwise it adds planning time and complexity. In PostgreSQL a primary key or unique index on a partitioned table must include the partition key, so <code>order_id</code> alone cannot be unique across partitions. Never partition just because the table is big; first check indexes and statistics.")}
<h3>N+1 and the slow-query log</h3>
<p>The N+1 problem (Section 10.4) is the most common reason an application is slow with a fast database: one query lists 100 orders, then the code runs 100 more queries, one per order. The cure is one join or one <code>WHERE id IN (...)</code> query. To find such patterns in PostgreSQL, enable the <code>pg_stat_statements</code> extension (not run here): it adds up calls, total time and mean time per query shape, so a cheap query called 2 million times shows up at the top. Sort by <code>total_exec_time</code>, not by the slowest single query, because the biggest cost is often a million quick calls.</p>
<h3>Practice with answers</h3>
{qa("10.6.2","A <code>WHERE status = 'open'</code> query is slow on a 300 million row table where 0.2 percent of rows are open. What index? <em>(medium)</em>","A partial index: <code>CREATE INDEX ON t (id) WHERE status = 'open'</code>. It holds only 0.2 percent of rows (600,000 entries), so it is tiny and fast to maintain. The query must repeat <code>status = 'open'</code> for the planner to use it.")}
{qa("10.6.3","What is wrong with <code>SELECT * FROM t ORDER BY created DESC LIMIT 20 OFFSET 100000</code> and what is the fix? <em>(medium)</em>","The database reads and discards 100,000 rows before returning 20. Fix: keyset pagination, <code>WHERE (created, id) &lt; (:last_created, :last_id) ORDER BY created DESC, id DESC LIMIT 20</code>, backed by an index on <code>(created, id)</code>.")}
{qa("10.6.4","A query that was fast last month now takes minutes, and no code changed. List three causes in the order you would check them. <em>(interview)</em>","(1) Stale statistics after data growth or a bulk load: run <code>ANALYZE</code> and compare estimated with actual rows. (2) A plan that flipped because the data distribution changed (skew), seen by comparing old and new <code>EXPLAIN ANALYZE</code>. (3) Table or index bloat from many updates without vacuum, or a lock wait: check <code>pg_stat_activity</code> for blocked sessions before blaming the plan. Others: a missing index on a new join column, or the data growing beyond memory so a hash join spills to disk.")}
{qa("10.6.5","Why can a covering index make a query faster than any other index, and what is its cost? <em>(expert)</em>","If the index contains every column the query needs, the database never visits the table (an index-only scan), which avoids one random read per row. The costs are a larger index, slower writes (every insert and update of those columns also updates the index), and in PostgreSQL index-only scans still check the visibility map, so they work best on well-vacuumed, mostly static tables.")}
'''
insert("10","lab10",body)
