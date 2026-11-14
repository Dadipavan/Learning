from _kit import *
import re
c=lambda s: "<code>%s</code>" % e(s)
parts=[]
def H(t): parts.append("<h3>%s</h3>" % t)
parts.append('<h2 id="x-expert-rows">Expert Rows: Isolation, Security, Index Types, Patterns, Types and Dialects</h2>')
parts.append("<p>These rows summarise the expert sections added to Chapters 2, 4, 7 to 16. Items marked (PG) are PostgreSQL; check the manual for MySQL and SQL Server details.</p>")
H("Isolation levels and anomalies (PG)")
parts.append(tbl(["Problem","READ COMMITTED","REPEATABLE READ","SERIALIZABLE"],[
["Dirty read","prevented","prevented","prevented"],["Non-repeatable read","possible","prevented","prevented"],["Phantom read","possible","prevented (snapshot)","prevented"],["Lost update (read, then write in the app)","possible","error, retry","error, retry"],["Write skew","possible","possible","error, retry"]]))
parts.append("<p>Retry on SQLSTATE 40001 (serialization failure) and 40P01 (deadlock): rerun the whole transaction with backoff and jitter. Atomic update: %s. Job queue: %s.</p>" % (c("SET x = x - 100"), c("FOR UPDATE SKIP LOCKED")))
H("Security and access")
parts.append(tbl(["Task","Pattern"],[
["Stop SQL injection","placeholders for values (%s or %s); allow-list for identifiers and sort direction" % (c("?"),c("%s"))],
["Least privilege","one role per job: "+c("CREATE ROLE analyst NOLOGIN; GRANT SELECT ON t TO analyst;")],
["Hide columns or rows",c("CREATE VIEW v AS SELECT ... WHERE ...")+", grant on the view only"],
["Row-level security (PG)",c("ALTER TABLE t ENABLE ROW LEVEL SECURITY; CREATE POLICY p ON t USING (tenant_id = ...)")],
["Multi-tenant safety",c("tenant_id")+" in every primary and foreign key"]]))
H("Index types and plans (Chapter 10)")
parts.append(tbl(["Need","Use"],[
["Equality and ranges","B-tree (default)"],["Arrays, jsonb, full text","GIN"],["Geometry, nearest neighbour","GiST"],["Huge append-only table in time order","BRIN"],["Only a few rows matter","partial index"],["Search on a function","expression index, e.g. "+c("lower(email)")],
["Slow "+c("OFFSET"),"keyset: "+c("WHERE (a, id) > (:a, :id) ORDER BY a, id LIMIT n")],["Bad row estimates",c("ANALYZE")+", raise statistics target, extended statistics"],["Remove old data fast","range partitions and "+c("DETACH PARTITION")]]))
H("Pattern library (Chapters 7, 12)")
parts.append(tbl(["Question shape","Pattern"],[
["Best N per group",c("row_number() OVER (PARTITION BY g ORDER BY x DESC)")+" in a CTE, then "+c("rn <= N")],
["Path in a graph","recursive CTE, path string as cycle guard, depth limit"],
["Bill of materials","recursive CTE multiplying "+c("need * qty")+", then "+c("sum")+" over leaf parts"],
["Median or p90","row_number and count, or "+c("percentile_cont")+" (PG)"],
["Overlap test",c("a.s < b.e AND b.s < a.e")],
["Merge intervals","running "+c("max(end)")+" of earlier rows; new block when start is greater"],
["Running distinct count",c("row_number() OVER (PARTITION BY uid ORDER BY ts) = 1")+" flag, then running sum"],
["Did all of these",c("HAVING count(DISTINCT x) = (SELECT count(*) FROM required)")],
["Subtotals",c("ROLLUP")+", "+c("CUBE")+", "+c("GROUPING SETS")+"; label with "+c("GROUPING()")],
["Unknown pivot columns","build the SQL in code from "+c("SELECT DISTINCT")]]))
H("NULL, ordering and types (Chapter 2)")
parts.append(tbl(["Trap","Safe form"],[
[c("col <> 'x'")+" drops NULL rows",c("col IS DISTINCT FROM 'x'")+" (PG), "+c("IS NOT")+" (SQLite)"],
[c("NOT IN")+" with a NULL in the subquery",c("NOT EXISTS")],
["NULL sort position differs by engine",c("ORDER BY x NULLS LAST")],
["Case-sensitive text compare",c("lower(a) = lower(b)")+" or a case-insensitive collation"],
["Integer division",c("100.0 * a / b")]]))
H("Modelling and join sanity (Chapters 4, 11)")
parts.append(tbl(["Rule","Meaning"],[
["Rows after a join","one row per matching pair; one-to-many joins multiply rows"],
["Check after each join",c("count(*)")+" versus "+c("count(DISTINCT key)")],
["BCNF test","every dependency X -&gt; Y needs a superkey X; closure of X equal to all columns means superkey"],
["Lossless split","the shared columns must be a key of one piece"],
["Soft delete","partial unique index "+c("WHERE deleted_at IS NULL")]]))
H("Dialect quick map (Chapter 14.6)")
parts.append(tbl(["Task","Common form","Differs in"],[
["Top N",c("LIMIT n"),"SQL Server "+c("TOP n")+", Oracle "+c("FETCH FIRST n ROWS ONLY")],
["Upsert",c("ON CONFLICT"),"MySQL "+c("ON DUPLICATE KEY UPDATE")+", others "+c("MERGE")],
["String aggregate",c("string_agg"),"MySQL "+c("GROUP_CONCAT")+", Oracle and Snowflake "+c("LISTAGG")],
["Month bucket",c("date_trunc('month', d)"),"MySQL "+c("DATE_FORMAT")+", Oracle "+c("TRUNC(d, 'MM')")],
["Top 1 per group shortcut",c("QUALIFY"),"BigQuery, Snowflake, DuckDB only"]]))
body="\n".join(parts)
path=ROOT+"appendix.html"
s=open(path).read()
a,b="<!-- gen:app -->","<!-- /gen:app -->"
blk=a+"\n"+body+"\n"+b+"\n"
if a in s: s=re.sub(re.escape(a)+".*?"+re.escape(b)+"\n",lambda m:blk,s,flags=re.S)
else:
    m=re.search(r'<h2 id="s15-an-honest-closing-note">',s); assert m
    s=s[:m.start()]+blk+s[m.start():]
open(path,"w").write(s); print("ok")
