<p>On Tuesday morning the CEO's question is answered, but on Wednesday the finance team sends a fresh export of <code>orders.csv</code> and the numbers move. Somebody pasted new rows under old ones; somebody else filtered the file and saved it under the same name; a third person cannot say which version was used for last week's slides. Nobody was careless. The team simply has no <em>process</em> that turns a file into a trusted table. That process is data engineering, and it is the quiet half of every analytics and machine learning project.</p>
<p>In this chapter you will take ShopKart's flat files and build a small, repeatable, checked pipeline: define a schema, load the tables into a database, add keys and indexes, load new data incrementally without creating duplicates, run quality checks that stop bad data at the door, and wrap it all in one script that you can schedule. You will meet each idea in SQL and pandas (run here) and see the Excel, Power BI and R versions (not run here). After the chapter you will know what a warehouse table is, why a load must be <em>idempotent</em>, and what to put in a quality check.</p>

<h2>2.1 From files to tables: what engineering adds</h2>
<p>A file is data at rest in one shape. A table in a database is data with rules: every column has a type, a key makes rows unique, a constraint can reject nonsense, an index makes searches fast, and a transaction guarantees that a load either fully happens or not at all. Engineering is the work of moving from the first to the second, again and again, without surprises.</p>
@@table
Concept | Plain meaning | ShopKart example
Source | Where data originates | Operations export of orders, CRM export of customers
Ingest | Copy it into your control | Read the CSV, write a raw table
Raw layer | Untouched copy, kept for audit | <code>raw_orders</code>
Clean layer | Typed, deduplicated, standardised | <code>orders</code> (Chapter 3 rules)
Mart | Tables shaped for questions | <code>daily_city_sales</code>
Orchestration | Scheduling and ordering of steps | Run every night at 02:00
Idempotent | Running twice gives the same result as once | Reloading the same file adds no rows
@@
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">Think of three shelves in a kitchen. The delivery box on the floor is raw (never throw it away until you are sure). The shelf of washed, labelled jars is clean. The plated dish is the mart, ready for the guest. Each step reads only from the shelf below.</div></div>

<h2>2.2 Designing the schema</h2>
<p>The process: (1) list the <em>entities</em> (orders, customers, products); (2) pick a <strong>primary key</strong> for each (the column that identifies a row); (3) put attributes with the entity they describe; (4) connect entities with <strong>foreign keys</strong>; (5) choose types. This arrangement, a central fact table (orders) surrounded by dimension tables (customers, products), is called a star schema, and it is what Power BI's model view and most warehouses expect.</p>
<p class="problem"><span class="pl">Problem 2.2.1</span> Create a typed database for ShopKart with primary and foreign keys and load the three CSV files into it. Report row counts.</p>
@@steps
Step 1 | Write <code>CREATE TABLE</code> statements with types, <code>PRIMARY KEY</code> and <code>FOREIGN KEY</code>.
Step 2 | Turn on foreign-key checking (SQLite needs <code>PRAGMA foreign_keys = ON</code>).
Step 3 | Read the CSV with pandas and clean the minimum (drop exact duplicates, since the key would otherwise reject them).
Step 4 | Insert with <code>to_sql(..., if_exists="append")</code> and count rows.
@@
@@py
import sqlite3, pandas as pd

DDL = """
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, signup_date TEXT NOT NULL, segment TEXT, age REAL);
CREATE TABLE products  (product_id INTEGER PRIMARY KEY, product TEXT UNIQUE NOT NULL, category TEXT, list_price REAL, unit_cost REAL, description TEXT);
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date TEXT NOT NULL, order_hour INTEGER, city TEXT, channel TEXT, category TEXT,
    product TEXT REFERENCES products(product), quantity INTEGER CHECK (quantity > 0),
    unit_price REAL, discount REAL CHECK (discount BETWEEN 0 AND 1), status TEXT,
    promised_minutes REAL, delivery_minutes REAL);
"""
con = sqlite3.connect(":memory:")
con.execute("PRAGMA foreign_keys = ON")
con.executescript(DDL)
for t in ["customers", "products", "orders"]:
    df = pd.read_csv(DATA + t + ".csv")
    if t == "orders":
        df = df.drop_duplicates()
    df.to_sql(t, con, if_exists="append", index=False)
    print(t, con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
@@
<p>The load succeeded, which tells us something already: every customer id and every product in the orders file exists in the dimension tables (the foreign keys would have complained), all quantities are positive and discounts lie between 0 and 1. Constraints are free quality checks that run on every insert.</p>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Skipping the key because "the data is fine".</strong> Wrong: loading without a primary key, so the 150 duplicate orders sit silently in the table and inflate revenue. Right: declare <code>order_id</code> as the key; the database then rejects a second copy and you learn about the problem on day one. (Here we dropped exact duplicates first, because inserting them would fail.)</div></div>

<h3>The same design in other tools (not run here)</h3>
@@table
Tool | How you express the schema | Notes
Excel | Convert each range to a Table (Ctrl+T); in Power Pivot choose Manage Data Model, Diagram View, drag <code>Orders[customer_id]</code> onto <code>Customers[customer_id]</code> | A relationship is the Excel equivalent of a foreign key, but it does not reject bad rows
Power BI | Model view: drag the key columns to create a one-to-many relationship from Customers to Orders; set cross filter direction to Single | The "one" side must contain unique values
R | <code>DBI::dbExecute(con, ddl)</code> then <code>dbWriteTable(con, "orders", orders, append = TRUE)</code> | Same SQL, any database
@@

<h2>2.3 Loading: full, incremental and idempotent</h2>
<p>A <strong>full load</strong> replaces the whole table. It is simple and safe for small data, but wasteful when tomorrow's file adds 60 rows to 20,000. An <strong>incremental load</strong> adds only what is new, found with a <strong>watermark</strong>: the largest <code>order_date</code> already loaded. The danger is the word "only": if the job crashes and reruns, or the same file arrives twice, a naive append doubles the rows. The cure is an <strong>upsert</strong>: insert new keys, update existing ones.</p>
<p class="problem"><span class="pl">Problem 2.3.1</span> Load January to June, then load the full year file as if a second delivery had arrived (it overlaps the first). Show that an upsert produces exactly the right row count and that a naive append does not.</p>
@@steps
Setup | Table with <code>order_id</code> as primary key; first load holds 1 Jan to 30 Jun.
Naive | <code>INSERT</code> the whole year file: the primary key rejects the overlap and the job fails (or, without a key, duplicates appear).
Upsert | <code>INSERT ... ON CONFLICT(order_id) DO UPDATE</code> accepts overlap and updates in place.
Check | Row count after the second load equals the distinct order ids in the file.
@@
@@py
import sqlite3, pandas as pd

df = pd.read_csv(DATA + "orders.csv").drop_duplicates()
cols = list(df.columns)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, order_hour INT, city TEXT, channel TEXT, category TEXT, product TEXT, quantity INT, unit_price REAL, discount REAL, status TEXT, promised_minutes REAL, delivery_minutes REAL)")

def upsert(con, frame):
    sets = ", ".join(f"{c}=excluded.{c}" for c in cols if c != "order_id")
    sql = f"INSERT INTO orders ({','.join(cols)}) VALUES ({','.join('?'*len(cols))}) ON CONFLICT(order_id) DO UPDATE SET {sets}"
    rows = [tuple(None if pd.isna(v) else v for v in r) for r in frame.itertuples(index=False, name=None)]
    con.executemany(sql, rows)
    con.commit()

first = df[df.order_date < "2024-07-01"]
upsert(con, first)
print("after first load :", con.execute("SELECT COUNT(*), MAX(order_date) FROM orders").fetchone())

try:
    con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [tuple(None if pd.isna(v) else v for v in r) for r in df.itertuples(index=False, name=None)])
except sqlite3.IntegrityError as e:
    print("naive append     : rejected ->", e)
    con.rollback()

upsert(con, df)
upsert(con, df)   # run it twice on purpose
print("after 2 upserts  :", con.execute("SELECT COUNT(*), MAX(order_date) FROM orders").fetchone(), "| distinct ids in file:", df.order_id.nunique())
@@
<p>Running the upsert twice changes nothing: that is idempotence. It is the single most useful property of a pipeline, because every real pipeline eventually runs twice (a retry, a manual rerun, a scheduler glitch).</p>
<h3>Watermarks in practice</h3>
<p>To fetch only new rows from a source database, remember the last loaded date and ask for rows after it: <code>SELECT * FROM orders WHERE order_date &gt; :watermark</code>. Two traps: late-arriving rows (an order dated 30 June that reaches the source on 2 July is missed), and updates (a status changing from delivered to returned). Safer patterns reload a sliding window, say the last 7 days, using an upsert so overlaps are harmless.</p>
@@table
Pattern | How | Good for | Risk
Full reload | Drop and rebuild | Small tables, simplicity | Slow, brief empty table
Append only | Insert rows after watermark | Immutable events (clicks) | Duplicates on rerun, misses updates
Upsert window | Reload last N days with upsert | Orders whose status changes | Choose N larger than the longest delay
Change data capture | Read the source's change log | Large systems | More infrastructure
@@
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Design every load so that running it twice equals running it once. Then retries are safe, and you can fix a bug and simply rerun history.</div></div>

<h2>2.4 Indexes and the shape of a query</h2>
<p>Without an index, SQLite reads every row to find a customer's orders. With an index on <code>customer_id</code> it jumps straight to them, like a book index versus reading every page. The tool that shows the difference is <code>EXPLAIN QUERY PLAN</code>, and a simple timer shows the effect on our 20,000 rows.</p>
@@py
import sqlite3, time

con = sqlite3.connect(":memory:")
sqlite3.connect(DATA + "shopkart.db").backup(con)   # work on a copy, leave the file untouched
q = "SELECT COUNT(*), SUM(quantity) FROM orders WHERE customer_id = 1500"
print(con.execute("EXPLAIN QUERY PLAN " + q).fetchall()[0][3])

def timeit(n=2000):
    t = time.perf_counter()
    for _ in range(n):
        con.execute(q).fetchone()
    return (time.perf_counter() - t) / n * 1e6

before = timeit()
con.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id)")
print(con.execute("EXPLAIN QUERY PLAN " + q).fetchall()[0][3])
after = timeit()
con.execute("DROP INDEX idx_orders_customer")
print("index made the lookup faster:", before > 3 * after)
@@
<p>The first plan says <code>SCAN orders</code> (every row), the second says <code>SEARCH orders USING INDEX</code>. We print only whether it became at least three times faster because exact microseconds depend on your machine. (We worked on an in-memory copy so the shared database file stays unchanged.) The price of an index is slower inserts and extra storage, so index the columns you filter and join on, not everything.</p>
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">A common first task for a data engineer is not building something new but finding why the nightly report takes 40 minutes. The answer is often a missing index, a join on mismatched types (text against integer), or a query that pulls all columns when two are needed.</div></div>

<h2>2.5 Data quality checks that stop bad data</h2>
<p>A quality check is a small test with a name, a rule and a severity. Run the checks after ingest and before anything downstream reads the table. Six families cover most needs.</p>
@@table
Family | Question | ShopKart rule
Completeness | Is anything missing that should not be? | <code>order_date</code> never null; city missing under 1 percent
Uniqueness | Are keys unique? | <code>order_id</code> unique after dedupe
Validity | Are values in the allowed set or range? | status in delivered, returned, cancelled; discount between 0 and 1
Consistency | Do tables agree? | every order's customer exists
Timeliness | Is the data fresh? | latest order date within 2 days of the run date
Volume | Is the row count plausible? | daily orders within a band around the usual
@@
<p class="problem"><span class="pl">Problem 2.5.1</span> Write a function that runs these checks on the raw orders file and reports pass or fail for each, with the offending count.</p>
@@steps
Step 1 | Express each rule as a pandas boolean that marks the offending rows.
Step 2 | A check passes when the offender count is at or below a tolerance.
Step 3 | Print a report; in a pipeline you would raise an error for severe failures and only warn for mild ones.
@@
@@py
import pandas as pd

def run_checks(o, c):
    checks = [
        ("order_date not null",      o.order_date.isna().sum(), 0),
        ("order_id unique",          o.order_id.duplicated().sum(), 0),
        ("status in allowed set",    (~o.status.isin(["delivered", "returned", "cancelled"])).sum(), 0),
        ("discount within 0..1",     (~o.discount.between(0, 1)).sum(), 0),
        ("quantity 1..20",           (~o.quantity.between(1, 20)).sum(), 0),
        ("customer exists",          (~o.customer_id.isin(c.customer_id)).sum(), 0),
        ("city missing (<1%)",       o.city.isna().sum(), int(0.01 * len(o))),
        ("delivery time 5..300 min", (~o.delivery_minutes.dropna().between(5, 300)).sum(), 0),
    ]
    return pd.DataFrame(checks, columns=["check", "offenders", "tolerance"]).assign(
        result=lambda d: (d.offenders <= d.tolerance).map({True: "pass", False: "FAIL"}))

o = pd.read_csv(DATA + "orders.csv")
c = pd.read_csv(DATA + "customers.csv")
print(run_checks(o, c).to_string(index=False))
@@
<p>Three checks fail on the raw file: duplicated ids, absurd quantities, and impossible delivery times. That is the right result: the checks found precisely the faults we planted. In Chapter 3 you will fix them; in the pipeline of Section 2.6 the same function guards the door.</p>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Checks that nobody reads.</strong> Wrong: printing a report into a log that no one opens, so a broken feed runs for weeks. Right: classify rules as blocking (stop the pipeline) or warning (notify), send the result to a channel people watch, and track the number of failures over time.</div></div>

<h3>Going deeper: contracts and expectations</h3>
<p>Mature teams write the rules as a <em>data contract</em> agreed with the producer of the data ("status is one of three values; order_id never repeats"), and use libraries that express the same checks as declarative "expectations". The principle is identical to our function: rules as data, results as a table, failures route to an owner. Tools such as Great Expectations or dbt tests implement it (not run here).</p>

<h2>2.6 A small pipeline you can schedule</h2>
<p>Now we assemble the pieces into one script with five steps: <em>extract</em> (read), <em>validate</em> (checks on raw), <em>transform</em> (clean rules from Chapter 3), <em>load</em> (upsert into a warehouse file), and <em>publish</em> (build a mart table). Each step is a function, each logs one line, and the whole is idempotent.</p>
@@py
import sys, sqlite3, tempfile, os
import pandas as pd
sys.path.insert(0, DATA)
import prep

def extract():
    o, c, p = prep.load_raw(DATA)
    return o, c, p

def validate(o, c):
    bad_keys = (~o.customer_id.isin(c.customer_id)).sum()
    assert bad_keys == 0, f"{bad_keys} orders with unknown customers"
    assert o.order_date.notna().all(), "missing order dates"
    return {"rows_in": len(o)}

def transform():
    return prep.load_clean(DATA)

def load(wh, o, c, p):
    for name, df in (("orders", o), ("customers", c), ("products", p)):
        d = df.copy()
        for col in d.columns:
            if str(d[col].dtype).startswith("datetime"):
                d[col] = d[col].dt.strftime("%Y-%m-%d")
        d.to_sql(name, wh, if_exists="replace", index=False)   # full reload per run, idempotent

def publish(wh):
    wh.execute("DROP TABLE IF EXISTS daily_city_sales")
    wh.execute("""CREATE TABLE daily_city_sales AS
                  SELECT order_date, city, COUNT(*) AS orders, ROUND(SUM(revenue), 2) AS revenue
                  FROM orders GROUP BY order_date, city""")

def run(wh):
    o, c, p = extract()
    stats = validate(o, c)
    o2, c2, p2 = transform()
    load(wh, o2, c2, p2)
    publish(wh)
    stats["rows_out"] = wh.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    stats["mart_rows"] = wh.execute("SELECT COUNT(*) FROM daily_city_sales").fetchone()[0]
    return stats

path = os.path.join(tempfile.mkdtemp(), "warehouse.db")
wh = sqlite3.connect(path)
print("run 1:", run(wh))
print("run 2:", run(wh))
print(wh.execute("SELECT * FROM daily_city_sales ORDER BY revenue DESC LIMIT 3").fetchall())
@@
<p>Two runs give the same numbers, as an idempotent job must. The mart table <code>daily_city_sales</code> is what a dashboard should read: small, clean, one row per day and city. Notice that the mart contains rows with <code>city = None</code> (we cannot assign 120 orders to a city); a good pipeline would count these and alert if their share grew.</p>
<h3>Scheduling and orchestration (not run here)</h3>
<p>To run the script every night you have three levels. A <strong>cron</strong> line: <code>0 2 * * * /usr/bin/python3 /opt/shopkart/pipeline.py</code> (02:00 daily). A <strong>workflow tool</strong> such as Airflow, where each function becomes a task with dependencies (<code>extract &gt;&gt; validate &gt;&gt; transform &gt;&gt; load &gt;&gt; publish</code>), retries and alerts. A <strong>cloud scheduler</strong> (Power BI refresh, Azure Data Factory, a cloud function) that triggers the same code. Start with cron; move up when you need retries, backfills and a picture of dependencies.</p>
@@table
Need | Excel | Power BI | R / scripts
Refresh on a schedule | Power Query refresh on open; Power Automate or Task Scheduler for more | Scheduled refresh in the service (needs a gateway for on-premises files) | cron or Task Scheduler running an R or Python script
Reuse transformation steps | Query steps recorded in Power Query | Same Power Query steps, plus dataflows to share them | Functions and packages
Version control | Hard (binary workbook) | Possible with project files | Natural (text, Git)
@@

<h2>2.7 File formats and where data lives</h2>
<p>CSV is readable and universal, but it has no types, no compression and no schema. Analytical systems prefer <strong>columnar</strong> formats such as Parquet: values of one column are stored together, so a query that needs two of fourteen columns reads far less, and types survive the round trip. Our file sizes make the point on a small scale.</p>
@@py
import os, sqlite3, pandas as pd
for f in ["orders.csv", "customers.csv", "products.csv", "shopkart.db"]:
    print(f"{f:15s}{os.path.getsize(DATA + f)/1024:9.0f} KB")
df = pd.read_csv(DATA + "orders.csv")
print("in memory as read     :", round(df.memory_usage(deep=True).sum() / 1024), "KB")
small = df.assign(city=df.city.astype("category"), channel=df.channel.astype("category"), category=df.category.astype("category"),
                  product=df["product"].astype("category"), status=df.status.astype("category"),
                  quantity=df.quantity.astype("int16"), order_hour=df.order_hour.astype("int8"))
print("after category dtypes :", round(small.memory_usage(deep=True).sum() / 1024), "KB")
@@
<p>Choosing smaller types (<code>category</code> for repeated text, <code>int8</code> for hours) cuts memory in pandas by a large factor at no loss of information. Writing Parquet would be <code>df.to_parquet("orders.parquet")</code>, which needs the <code>pyarrow</code> package (not installed here, so not run here).</p>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">Rows are good for "fetch one order" (databases for transactions). Columns are good for "sum revenue over a million orders" (warehouses for analysis). Storage layout follows the question you ask most.</div></div>

<h2>2.8 Choosing the right tool for engineering tasks</h2>
@@table
Task | SQL / database | pandas | Excel | Power BI
Define a schema and keys | DDL, strongest | Only dtypes | Tables and relationships | Model view relationships
Load a file | <code>.import</code> or <code>to_sql</code> | <code>read_csv</code> | Get Data | Get Data
Incremental load | Upsert, watermarks | Manual logic | Poor | Incremental refresh (Premium or Pro setup)
Data quality checks | Constraints, queries | Boolean masks | Conditional formatting, manual | Column quality and profile panes
Schedule | cron, Airflow | cron, Airflow | Manual or Power Automate | Service refresh
@@
<p>The rule: put repeatable, shared, large-scale work in databases and scripts; keep Excel for small checks and hand-offs. The deepest idea of this chapter is not any command, it is that every step must be <em>re-runnable</em>.</p>

<h2>Chapter recap</h2>
<ul><li>Engineering turns files into trusted tables: types, keys, constraints, indexes, transactions.</li><li>Layer your data: raw, clean, mart. Never overwrite raw.</li><li>A star schema has a fact table (orders) and dimensions (customers, products).</li><li>Full loads are simple; incremental loads need a watermark and usually a sliding window.</li><li>An upsert (<code>ON CONFLICT DO UPDATE</code>) makes loads idempotent.</li><li>An index replaces a full scan with a search; use <code>EXPLAIN QUERY PLAN</code> to see which you get.</li><li>Quality checks come in six families: completeness, uniqueness, validity, consistency, timeliness, volume.</li><li>Distinguish blocking from warning checks and make results visible.</li><li>A pipeline is small functions: extract, validate, transform, load, publish.</li><li>Columnar formats and compact dtypes save memory and time.</li></ul>
@@table
Pattern | Meaning
<code>PRIMARY KEY</code>, <code>FOREIGN KEY</code> | Uniqueness and referential integrity enforced by the database
<code>INSERT ... ON CONFLICT DO UPDATE</code> | Idempotent upsert
<code>EXPLAIN QUERY PLAN</code> | Shows SCAN (slow) or SEARCH USING INDEX (fast)
Watermark | Largest loaded date; combine with a reload window
Check = rule + tolerance + severity | A named, automated test of the data
@@

<h2>Practice set</h2>
@@qa 2.9
Q: Name the three layers of a simple warehouse and say which one you never overwrite.
A: Raw, clean and mart. Never overwrite raw, because it is your audit trail and the source for re-running cleaning rules.
Q: What does idempotent mean, in one sentence, and why does a pipeline need it?
A: Running the job twice gives the same result as running it once; retries and reruns are inevitable, so they must be safe.
Q: Which ShopKart column is the primary key of orders, and which column links an order to a customer?
A: <code>order_id</code> is the primary key; <code>customer_id</code> is a foreign key to customers.
Q: The raw file has ~~len(raw):,~~ rows but ~~raw.order_id.nunique():,~~ distinct ids. What does the primary key do when you insert all rows?
A: It rejects the ~~len(raw)-raw.order_id.nunique()~~ repeated ids with an IntegrityError, so you must deduplicate or upsert.
Q: Write the SQL that counts orders per city in the warehouse.
A: <code>SELECT city, COUNT(*) FROM orders GROUP BY city;</code> (cleaned cities, so there are only five groups plus NULL).
Q: A naive append of a file that overlaps previously loaded dates: what two outcomes are possible?
A: With a primary key, the load fails; without one, duplicate rows are inserted and revenue is overstated.
Q: Why use a sliding window (last 7 days) instead of a pure watermark?
A: Orders can arrive late or change status after being loaded; reloading a window with an upsert catches both.
Q: When is an index a bad idea?
A: On tiny tables, on columns never used in filters or joins, or on tables with very heavy writes, since each insert must also update the index.
Q: Define a validity check and a consistency check for ShopKart, with the SQL for one of them.
A: Validity: discount between 0 and 1. Consistency: every order has a customer. SQL: <code>SELECT COUNT(*) FROM orders o LEFT JOIN customers c USING(customer_id) WHERE c.customer_id IS NULL;</code>
Q: Find the bug: the pipeline drops and rebuilds the raw table every run.
A: Raw is no longer an audit copy; if the source changes or loses rows you cannot reproduce past results. Keep raw append-only or snapshot it by date.
Q: Why does a category dtype save memory for the city column?
A: Repeated strings are stored once and each row keeps a small integer code, instead of one Python string per row.
Q: Interview style: "A dashboard that read fine yesterday shows revenue doubled today. What do you check first?"
A: Row counts by load date and distinct versus total order ids, which reveal a duplicate load; then the last pipeline run log and whether a join multiplied rows.
@@

<h2>Prompt pack</h2>
@@prompt
You are my patient, practical professor. I am a working professional moving into data roles. Teach me data engineering basics with an online-shop example: schemas, primary and foreign keys, idempotent loads, watermarks, and data quality checks. Ask me one question at a time, wait for my answer, correct me kindly, and finish with a mini design exercise.
@@
@@prompt
Act as a senior data engineer. Review my pipeline design: [describe your source files, tables, load method and schedule]. Check for idempotence, late-arriving data, missing quality checks and any place where raw data is overwritten. Give me a prioritised list of fixes and one example SQL statement for the most important one.
@@
@@prompt
Run a mock interview for a data engineer role. Ask me, one at a time, about star schemas, incremental loading, upserts, indexes and data quality, using a retail orders table as the example. Give feedback after each answer, then a final grade with three topics to study.
@@
