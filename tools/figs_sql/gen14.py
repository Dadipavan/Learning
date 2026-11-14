from _kit import *
db=shop()
X=lambda c: exec_sql(db,c)
c=lambda s: "<code>%s</code>" % e(s)
t1=tbl(["Task","PostgreSQL","MySQL 8","SQLite"],[
["First day of month",c("date_trunc('month', d)"),c("DATE_FORMAT(d, '%Y-%m-01')"),c("date(d, 'start of month')")],
["Add 7 days",c("d + INTERVAL '7 days'"),c("DATE_ADD(d, INTERVAL 7 DAY)"),c("date(d, '+7 days')")],
["Days between",c("d2 - d1")+" (dates)",c("DATEDIFF(d2, d1)"),c("julianday(d2) - julianday(d1)")],
["Join strings in a group",c("string_agg(x, ', ')"),c("GROUP_CONCAT(x SEPARATOR ', ')"),c("group_concat(x, ', ')")],
["Concatenate",c("a || b"),c("CONCAT(a, b)")+" (|| means OR by default)",c("a || b")],
["Replace NULL",c("COALESCE(x, 0)"),c("COALESCE(x, 0)")+", "+c("IFNULL"),c("COALESCE(x, 0)")+", "+c("IFNULL")],
["Top N",c("LIMIT n")+" or "+c("FETCH FIRST n ROWS ONLY"),c("LIMIT n"),c("LIMIT n")],
["Upsert",c("INSERT ... ON CONFLICT (k) DO UPDATE"),c("INSERT ... ON DUPLICATE KEY UPDATE"),c("INSERT ... ON CONFLICT (k) DO UPDATE")],
["Auto id",c("GENERATED ALWAYS AS IDENTITY"),c("AUTO_INCREMENT"),c("INTEGER PRIMARY KEY")],
["Quote a name",c('"name"'),c("`name`"),c('"name"')+" or "+c("[name]")],
["Boolean type",c("BOOLEAN"),c("BOOLEAN")+" is an alias of TINYINT(1)","0 and 1 stored as integers"]])
t2=tbl(["Task","SQL Server","Oracle"],[
["First day of month",c("DATETRUNC(month, d)")+" (2022+) or "+c("DATEFROMPARTS(YEAR(d), MONTH(d), 1)"),c("TRUNC(d, 'MM')")],
["Add 7 days",c("DATEADD(day, 7, d)"),c("d + 7")],
["Days between",c("DATEDIFF(day, d1, d2)"),c("d2 - d1")],
["Join strings in a group",c("STRING_AGG(x, ', ')")+" (2017+)",c("LISTAGG(x, ', ') WITHIN GROUP (ORDER BY x)")],
["Concatenate",c("a + b")+" or "+c("CONCAT(a, b)"),c("a || b")],
["Replace NULL",c("ISNULL(x, 0)")+", "+c("COALESCE"),c("NVL(x, 0)")+", "+c("COALESCE")],
["Top N",c("SELECT TOP n ...")+" or "+c("OFFSET 0 ROWS FETCH NEXT n ROWS ONLY"),c("FETCH FIRST n ROWS ONLY")+" (12c+)"],
["Upsert",c("MERGE"),c("MERGE")],
["Auto id",c("IDENTITY(1,1)"),c("GENERATED AS IDENTITY")+" (12c+)"],
["Quote a name",c("[name]")+" or "+c('"name"'),c('"name"')],
["Boolean type",c("BIT"),"no boolean column before 23ai; use NUMBER(1) or CHAR(1)"]])
t3=tbl(["Task","BigQuery","Snowflake"],[
["First day of month",c("DATE_TRUNC(d, MONTH)"),c("DATE_TRUNC('month', d)")],
["Add 7 days",c("DATE_ADD(d, INTERVAL 7 DAY)"),c("DATEADD(day, 7, d)")],
["Days between",c("DATE_DIFF(d2, d1, DAY)"),c("DATEDIFF(day, d1, d2)")],
["Join strings in a group",c("STRING_AGG(x, ', ')"),c("LISTAGG(x, ', ')")],
["Concatenate",c("a || b")+" or "+c("CONCAT"),c("a || b")+" or "+c("CONCAT")],
["Replace NULL",c("IFNULL(x, 0)")+", "+c("COALESCE"),c("NVL(x, 0)")+", "+c("COALESCE")+", "+c("IFNULL")],
["Top N",c("LIMIT n"),c("LIMIT n")+" or "+c("TOP n")],
["Top 1 per group",c("QUALIFY ROW_NUMBER() OVER (...) = 1"),c("QUALIFY ROW_NUMBER() OVER (...) = 1")],
["Upsert",c("MERGE"),c("MERGE")],
["Pivot",c("PIVOT (SUM(x) FOR k IN ('a','b'))"),c("PIVOT (SUM(x) FOR k IN ('a','b'))")],
["Quote a name",c("`name`"),c('"name"')+" (upper-case by default)"]])
mrev=X("""SELECT date(order_date, 'start of month') AS month, sum(i.qty * i.unit_price) AS revenue
FROM orders o JOIN order_items i ON i.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY month ORDER BY month;""")
sk=X("""SELECT group_concat(name, ', ') AS pune_customers FROM (SELECT name FROM customers WHERE city = 'Pune' ORDER BY name);
SELECT date('2024-01-31', '+7 days') AS plus7, julianday('2024-03-01') - julianday('2024-02-01') AS days_between, 10 / 4 AS int_div;""")
body=f'''
<h2 id="x14-6-dialect-translation-tables-fifteen-common-tasks-and-engine-notes">14.6 Dialect Translation Tables: Common Tasks Across Seven Engines</h2>
{co("blue","INTUITION","Every SQL database speaks the same core and a different accent. The core (<code>SELECT</code>, <code>JOIN</code>, <code>GROUP BY</code>, windows, CTEs) moves anywhere. The accent shows in dates, strings, upserts, top-N and quoting, and those are exactly the places a copied query fails. These tables are a phrasebook for the accent. The SQLite column below was run; all other engines were <strong>not run here</strong> and follow their documentation.")}
<h3>PostgreSQL, MySQL and SQLite</h3>
{t1}
<h3>SQL Server and Oracle</h3>
{t2}
<h3>BigQuery and Snowflake</h3>
{t3}
{P("14.6.1","Write 'paid revenue per month' in SQLite (run), then translate it. Predict first: four months, with January smallest.")}
{mrev}
{steps([("Step 1","The only dialect-specific piece is the month bucket. The rest (<code>JOIN</code>, <code>WHERE</code>, <code>GROUP BY</code>, <code>sum</code>) is portable."),("Step 2","Check: the four monthly totals 2,260 + 2,520 + 2,980 + 4,900 add to 12,660, the total of all paid order lines."),("Translate","PostgreSQL and Snowflake: <code>date_trunc('month', o.order_date)</code>. BigQuery: <code>DATE_TRUNC(o.order_date, MONTH)</code>. MySQL: <code>DATE_FORMAT(o.order_date, '%Y-%m-01')</code>. SQL Server: <code>DATETRUNC(month, o.order_date)</code> or <code>DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1)</code>. Oracle: <code>TRUNC(o.order_date, 'MM')</code>. In PostgreSQL and SQL Server <code>order_date</code> must be a real date type for these to work, whereas in SQLite it is text.")])}
<p>Three quick SQLite checks of other cells in the table, run for real:</p>
{sk}
<h3>Other engines you will meet</h3>
<ul><li><strong>DuckDB</strong>: an embedded analytical database (like SQLite for analytics). It reads Parquet and CSV files directly (<code>SELECT * FROM 'file.parquet'</code>), follows PostgreSQL syntax closely, and supports <code>QUALIFY</code>, <code>PIVOT</code> and <code>GROUP BY ALL</code>. Not run here.</li><li><strong>Spark SQL, Trino/Presto, ClickHouse</strong>: query engines for large files and warehouses. Core SQL is the same, but date functions (<code>date_trunc</code>, <code>date_add</code>), array and map types, and the absence of enforced constraints differ. They run queries over data, they do not give transactional guarantees the way PostgreSQL does.</li><li><strong>CockroachDB, Google Spanner, YugabyteDB</strong>: distributed SQL databases ('NewSQL'). They offer PostgreSQL-style SQL with transactions spread across machines, at the price of extra latency per commit. Use them when one machine is not enough but you still need ACID.</li><li><strong>MariaDB</strong>: a MySQL fork. Close to MySQL 5.7 and 8.0 with some differences (for example sequences, and different JSON handling).</li></ul>
{co("red","COMMON MISTAKE","Assuming <code>||</code> concatenates strings everywhere. In MySQL (default mode) <code>||</code> is the logical OR, so <code>'a' || 'b'</code> returns 0, silently. In SQL Server <code>||</code> is a syntax error and <code>+</code> concatenates, but <code>+</code> with a NULL gives NULL while <code>CONCAT</code> ignores NULLs. Use <code>CONCAT(a, b)</code> when portability matters, and remember it treats NULL differently from <code>||</code> in PostgreSQL (where <code>||</code> with NULL gives NULL).")}
<h3>Practice with answers</h3>
{qa("14.6.2","Translate <code>SELECT name FROM customers ORDER BY signup_date DESC LIMIT 3</code> for SQL Server and Oracle. <em>(easy)</em>","SQL Server: <code>SELECT TOP 3 name FROM customers ORDER BY signup_date DESC</code>. Oracle 12c and later: <code>SELECT name FROM customers ORDER BY signup_date DESC FETCH FIRST 3 ROWS ONLY</code>. Both have to keep <code>ORDER BY</code>, otherwise 'top' is arbitrary.")}
{qa("14.6.3","Rewrite <code>SELECT dept, GROUP_CONCAT(name) FROM emp GROUP BY dept</code> (MySQL) for PostgreSQL, Snowflake and Oracle. <em>(easy)</em>","PostgreSQL: <code>string_agg(name, ',')</code>. Snowflake: <code>LISTAGG(name, ',')</code>. Oracle: <code>LISTAGG(name, ',') WITHIN GROUP (ORDER BY name)</code>. MySQL's default result is cut at 1024 characters (<code>group_concat_max_len</code>), which the others do not do.")}
{qa("14.6.4","A query using <code>QUALIFY</code> must run on PostgreSQL. How do you port it? <em>(medium)</em>","Put the window function in a CTE or subquery that exposes it as a column (<code>rn</code>), then filter in the outer <code>WHERE rn = 1</code>. <code>QUALIFY</code> is only a shortcut for that pattern.")}
{qa("14.6.5","Why do many teams write <code>CAST(x AS DATE)</code> rather than engine-specific date functions where possible? <em>(interview)</em>","<code>CAST</code> and <code>CURRENT_DATE</code>, <code>COALESCE</code>, <code>CASE</code>, <code>EXTRACT</code> are in the SQL standard, so they port unchanged. Engine-specific shortcuts (<code>IFNULL</code>, <code>NVL</code>, <code>DATEADD</code>) force a rewrite per engine. For code that must run on several engines, prefer standard functions or isolate dialect functions in one place (a dbt macro, a view).")}
'''
insert("14","lab14",body)
