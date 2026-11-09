<p>The data is clean. Meera wants answers: which category earns most, how revenue moves month to month, which customers keep coming back. You open your SQL editor, your colleague opens a notebook, the finance lead opens Excel, and the marketing manager opens Power BI. Four people, four tools, one dataset. If everything is done right the four numbers match. If not, the Monday meeting becomes a debate about whose number is correct instead of what to do next.</p>
<p>This chapter is the analytics core: the handful of operations that answer most business questions. <strong>Aggregate</strong> (group and summarise), <strong>join</strong> (combine tables), use <strong>window functions</strong> (compare each row with its neighbours), build <strong>cohorts</strong> and <strong>retention</strong> tables, and finally <strong>visualise</strong> the result. Every task is solved in SQL and pandas (with real output), often with plain Python as well, and shown as formulas for Excel and Power BI (DAX), cross-checked against the verified numbers. You will leave knowing how to get the same answer in every tool, which reads best, and what each one is for.</p>
<p>All blocks use the cleaned tables from <code>prep.py</code> (Chapter 3). The helper <code>prep.clean_db(DATA)</code> returns an in-memory SQLite database with tables <code>orders</code>, <code>customers</code> and <code>products</code>, with columns <code>revenue</code> (net value of delivered orders, 0 otherwise) and <code>late</code> already added.</p>

<h2>4.1 Aggregation: group, then summarise</h2>
<p>Aggregation is the question "for each X, what is the total or average of Y?". Three parts: the <em>grouping key</em> (category), the <em>measure</em> (revenue) and the <em>function</em> (sum). Everything else is syntax.</p>
<p class="problem"><span class="pl">Problem 4.1.1</span> Compute net revenue and order count by category, sorted by revenue, in SQL, pandas and plain Python, and verify equality.</p>
@@steps
Grain | One output row per category; five rows.
SQL | <code>GROUP BY category</code> with <code>SUM(revenue)</code> and <code>COUNT(*)</code>.
pandas | <code>groupby("category").agg(...)</code>.
Python | A <code>dict</code> keyed by category, add to it in a loop over rows.
Check | Round the three revenue lists and compare.
@@
@@py
import sys
sys.path.insert(0, DATA)
import prep
from collections import defaultdict

o, c, p = prep.load_clean(DATA)
con = prep.clean_db(DATA)

sql = con.execute("""SELECT category, ROUND(SUM(revenue)) AS revenue, COUNT(*) AS orders
                     FROM orders GROUP BY category ORDER BY revenue DESC""").fetchall()
pdf = (o.groupby("category").agg(revenue=("revenue", "sum"), orders=("order_id", "count"))
         .sort_values("revenue", ascending=False).round(0))

tot, cnt = defaultdict(float), defaultdict(int)
for cat, rev in zip(o["category"], o["revenue"]):
    tot[cat] += rev
    cnt[cat] += 1
py = sorted(((k, round(v), cnt[k]) for k, v in tot.items()), key=lambda t: -t[1])

print(pdf.to_string())
print("all three equal:", [(a, int(b), n) for a, b, n in sql] == [(k, int(r.revenue), int(r.orders)) for k, r in pdf.iterrows()] == [(a, int(b), n) for a, b, n in py])
@@
<p>The answer to Chapter 1's Q3: Fashion earns the most, with Electronics close behind, even though Grocery has nearly twice as many orders as either, because a Fashion or Electronics order is worth much more. Count alone would have crowned Grocery; value alone hides how many customers are involved. Always show both side by side.</p>
<h3>The same in Excel and Power BI (not run here)</h3>
@@table
Tool | How | Formula or steps
Excel formula | One cell per category | <code>=SUMIFS(Orders[revenue], Orders[category], A2)</code> and <code>=COUNTIFS(Orders[category], A2)</code> (cells A2 to A6 list the five categories)
Excel PivotTable | Insert, PivotTable, from the Orders table | Rows: category. Values: Sum of revenue, Count of order_id. Sort by value (right-click, Sort, Largest to Smallest)
DAX measure | Reusable, responds to slicers | <code>Revenue = SUM(Orders[revenue])</code> and <code>Orders = COUNTROWS(Orders)</code>; put <code>category</code> on a table visual and both measures as values
R | dplyr | <code>orders %&gt;% group_by(category) %&gt;% summarise(revenue = sum(revenue), n = n()) %&gt;% arrange(desc(revenue))</code>
@@
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">A PivotTable, a SQL <code>GROUP BY</code>, a pandas <code>groupby</code> and a DAX measure in a table visual are the same operation wearing four costumes. Learn the idea (key, measure, function) once and the syntax is a dictionary lookup, which is exactly what the appendix gives you.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Averaging averages.</strong> Wrong: average order value of the country = mean of the five city averages. Cities with few orders count as much as big ones. Right: total revenue ÷ total orders, or a weighted mean. In DAX this is why a measure <code>DIVIDE([Revenue], [Orders])</code> is correct and an average of an average column is not.</div></div>

<h2>4.2 Time: months, growth and seasonality</h2>
<p>Time questions need a period key (month), a measure, and often a comparison with the previous period. We compute monthly revenue and month-on-month growth.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep
o, c, p = prep.load_clean(DATA)
con = prep.clean_db(DATA)

q = """SELECT substr(order_date, 1, 7) AS month, ROUND(SUM(revenue)) AS revenue
       FROM orders GROUP BY 1 ORDER BY 1"""
sql = con.execute(q).fetchall()
m = o.groupby(o.order_date.dt.strftime("%Y-%m")).revenue.sum().round()
print("sql == pandas:", all(abs(a[1] - b) <= 1 for a, b in zip(sql, m)) and len(sql) == len(m))
g = (m.pct_change() * 100).round(1)
print(pd_out := m.astype(int).to_frame("revenue").assign(growth_pct=g).to_string())
print("best month:", m.idxmax())
@@
<p>Revenue climbs from January to a peak in August, falls through the autumn, jumps again in November (a late-November sales window is built into the data) and drops in December. The month-on-month percentage is noisy; to call a pattern seasonal you need several years, which we do not have. One year can show a shape but cannot prove that it repeats.</p>
@@table
Tool | Monthly revenue | Month-on-month growth
SQL | <code>GROUP BY substr(order_date,1,7)</code> | window <code>LAG(revenue) OVER (ORDER BY month)</code> (Section 4.4)
pandas | <code>resample("MS", on="order_date")</code> or groupby on <code>dt.to_period("M")</code> | <code>pct_change()</code>
Excel | PivotTable, drag order_date to Rows and group by Months and Years | Value Field Settings, Show Values As, % Difference From (Previous)
DAX | Needs a date table: <code>Dates = CALENDAR(DATE(2024,1,1), DATE(2024,12,31))</code>, related to Orders[order_date] | <code>MoM = DIVIDE([Revenue] - CALCULATE([Revenue], DATEADD(Dates[Date], -1, MONTH)), CALCULATE([Revenue], DATEADD(Dates[Date], -1, MONTH)))</code>
@@
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Power BI time intelligence (<code>DATEADD</code>, <code>SAMEPERIODLASTYEAR</code>, <code>DATESYTD</code>) requires a proper date table with every date and a relationship to the fact table. If a time measure returns blanks, check this first.</div></div>

<h2>4.3 Joins: combining tables, and the fan-out trap</h2>
<p>A join matches rows from two tables on a key. <strong>Inner join</strong> keeps matches only; <strong>left join</strong> keeps every left row, with missing on the right when no match. Which one you choose changes the row count, so always check the count before and after.</p>
<p class="problem"><span class="pl">Problem 4.3.1</span> Revenue by customer segment (join orders to customers), and how many customers never ordered (an anti-join).</p>
@@steps
Join key | <code>customer_id</code>, many orders to one customer.
Segment revenue | Inner join, group by segment.
Never ordered | Customers whose id is not in orders: <code>LEFT JOIN ... WHERE o.customer_id IS NULL</code> in SQL, <code>~isin</code> in pandas.
Check | Orders before and after the join must be equal.
@@
@@py
import sys
sys.path.insert(0, DATA)
import prep
o, c, p = prep.load_clean(DATA)
con = prep.clean_db(DATA)

print(con.execute("""SELECT c.segment, COUNT(*) AS orders, ROUND(SUM(o.revenue)) AS revenue
                     FROM orders o JOIN customers c ON c.customer_id = o.customer_id
                     GROUP BY c.segment ORDER BY revenue DESC""").fetchall())
j = o.merge(c, on="customer_id", how="inner")
print("rows before/after join:", len(o), len(j))
print(j.groupby("segment").agg(orders=("order_id", "count"), revenue=("revenue", "sum")).round(0).sort_values("revenue", ascending=False).to_dict("index"))

never_sql = con.execute("""SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
                           WHERE o.customer_id IS NULL""").fetchone()[0]
never_pd = (~c.customer_id.isin(o.customer_id)).sum()
print("customers who never ordered:", never_sql, never_pd)
@@
<p>Regular customers bring the most revenue in total because there are more of them; Premium customers spend more <em>per customer</em>. A good analyst reports both totals and per-customer figures. The anti-join shows that roughly one customer in five never ordered in 2024, which is a marketing question for Chapter 8's memo.</p>
<h3>Fan-out: the join that silently inflates revenue</h3>
<p>If the right table has more than one row per key, a join multiplies left rows. Suppose a table of promotions lists two campaigns per category. Joining orders to it duplicates each order, and revenue doubles.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep
import pandas as pd
o, c, p = prep.load_clean(DATA)
promo = pd.DataFrame({"category": ["Grocery", "Grocery", "Fashion", "Fashion", "Home", "Home", "Beauty", "Beauty", "Electronics", "Electronics"],
                      "campaign": ["A", "B"] * 5})
bad = o.merge(promo, on="category")
print("rows:", len(o), "->", len(bad), "| revenue:", round(o.revenue.sum()), "->", round(bad.revenue.sum()))
good = o.merge(promo.groupby("category").size().rename("n_campaigns").reset_index(), on="category")
print("one row per key keeps rows:", len(good), "| revenue:", round(good.revenue.sum()))
try:
    o.merge(promo, on="category", validate="m:1")
except Exception as e:
    print("validate caught it:", type(e).__name__)
@@
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Trusting a join without counting rows.</strong> Wrong: joining to a table with two rows per key and reporting revenue that is exactly twice the truth. Right: compare row counts before and after, assert uniqueness of the key on the "one" side (pandas <code>validate="m:1"</code>, SQL <code>SELECT key, COUNT(*) ... HAVING COUNT(*) &gt; 1</code>), and aggregate the many side before joining.</div></div>
<p>In Power BI the model protects you: a relationship is one-to-many and a measure sums the fact column, so a dimension with duplicate keys is refused at load time. In Excel, <code>XLOOKUP</code> returns the first match only (no fan-out, but it hides duplicates), while Power Query's Merge expands to every match (fan-out possible).</p>

<h2>4.4 Window functions: compare a row to its neighbours</h2>
<p>An aggregate collapses rows; a window function keeps every row and adds a calculation over a "window" of related rows. The typical cases: running totals, ranks within groups, previous-period comparisons and moving averages.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep
o, c, p = prep.load_clean(DATA)
con = prep.clean_db(DATA)

print("--- SQL: running total, previous month, top product per category")
q = """
WITH m AS (SELECT substr(order_date,1,7) AS month, SUM(revenue) AS rev FROM orders GROUP BY 1),
     w AS (SELECT month, rev, SUM(rev) OVER (ORDER BY month) AS running, LAG(rev) OVER (ORDER BY month) AS prev FROM m)
SELECT month, ROUND(rev), ROUND(running), ROUND(prev) FROM w
WHERE month IN ('2024-01','2024-02','2024-12')"""
for r in con.execute(q): print(r)

q2 = """
SELECT category, product, ROUND(rev) FROM (
  SELECT category, product, SUM(revenue) AS rev,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(revenue) DESC) AS rn
  FROM orders GROUP BY category, product) WHERE rn = 1 ORDER BY category"""
sql_top = con.execute(q2).fetchall()
for r in sql_top: print(r)

print("--- pandas")
m = o.groupby(o.order_date.dt.strftime("%Y-%m")).revenue.sum()
w = m.to_frame("rev").assign(running=m.cumsum(), prev=m.shift(1)).round(0)
print(w.loc[["2024-01", "2024-02", "2024-12"]].to_string())
g = o.groupby(["category", "product"]).revenue.sum().round(0).reset_index()
top = g.loc[g.groupby("category").revenue.idxmax()].sort_values("category")
print("top product per category equal:", all((a, b) == (a2, b2) and abs(r - r2) <= 1 for (a, b, r), (a2, b2, r2) in zip(sql_top, top.itertuples(index=False))))
@@
<p>Note where the filter sits: the window is computed in the CTE <code>w</code> and the <code>WHERE</code> comes after. SQL applies <code>WHERE</code> <em>before</em> window functions in the same query, so filtering to three months first would have produced a running total of those three months only. The running total for December is the whole-year revenue, as the pandas output shows. The SQL <code>OVER (ORDER BY month)</code> and the pandas <code>cumsum()</code> / <code>shift()</code> give identical numbers. <code>ROW_NUMBER() OVER (PARTITION BY category ...)</code> is the SQL form of "top one per group"; in pandas it is <code>idxmax</code> after a groupby, or <code>sort_values().groupby().head(1)</code>.</p>
<p><strong>A moving average smooths noise.</strong> The 7-day average of daily orders is the standard way to read a jumpy daily series.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep
import numpy as np
o, c, p = prep.load_clean(DATA)
con = prep.clean_db(DATA)

sql = con.execute("""
SELECT d, ROUND(AVG(n) OVER (ORDER BY d ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 4)
FROM (SELECT order_date AS d, COUNT(*) AS n FROM orders GROUP BY order_date) ORDER BY d""").fetchall()
daily = o.groupby("order_date").size()
ma = daily.rolling(7, min_periods=1).mean().round(4)
print("days:", len(daily), "| equal:", np.allclose([r[1] for r in sql], ma.values))
print("last day raw", daily.iloc[-1], "| 7-day average", round(ma.iloc[-1], 2))

loop = []
vals = list(daily.values)
for i in range(len(vals)):
    window = vals[max(0, i - 6): i + 1]
    loop.append(sum(window) / len(window))
print("plain Python loop equal:", np.allclose(loop, ma.values))
@@
<p>All three agree. The SQL frame <code>ROWS BETWEEN 6 PRECEDING AND CURRENT ROW</code> is the exact analogue of <code>rolling(7, min_periods=1)</code> and of slicing the previous six values in the loop. The first six days use fewer than seven values in each version, which is why <code>min_periods=1</code> matters.</p>
@@table
Need | SQL | pandas | Excel | DAX
Running total | <code>SUM(x) OVER (ORDER BY d)</code> | <code>cumsum()</code> | <code>=SUM($B$2:B2)</code> filled down | <code>CALCULATE([Revenue], DATESYTD(Dates[Date]))</code> for year to date
Previous row | <code>LAG(x)</code> | <code>shift(1)</code> | <code>=B2</code> in the next row (offset reference) | <code>CALCULATE([Revenue], DATEADD(Dates[Date], -1, MONTH))</code>
Rank in group | <code>RANK() OVER (PARTITION BY g ORDER BY x DESC)</code> | <code>groupby(g).x.rank(ascending=False)</code> | <code>=COUNTIFS(G:G,G2,X:X,"&gt;"&amp;X2)+1</code> | <code>RANKX(ALLSELECTED(Products[product]), [Revenue])</code>
Moving average | <code>AVG(x) OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)</code> | <code>rolling(7).mean()</code> | <code>=AVERAGE(B2:B8)</code> filled down | <code>AVERAGEX(DATESINPERIOD(Dates[Date], MAX(Dates[Date]), -7, DAY), [Orders])</code>
@@
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Window over the wrong order.</strong> Wrong: a running total on a table sorted by product instead of date, so "cumulative revenue" jumps around. Right: state the order inside the window (<code>ORDER BY month</code>), never rely on how the table happens to be sorted. In SQL, without ORDER BY inside OVER, the frame is the whole partition.</div></div>

<h2>4.5 Cohorts and retention</h2>
<p>A <strong>cohort</strong> is a group of customers who share a starting point, here the month of their first order in the data. <strong>Retention</strong> asks: of the customers in the cohort, what share ordered again k months later? It separates "we have more orders because we have more customers" from "customers stay".</p>
@@steps
Step 1 | Find each customer's first order month: the cohort.
Step 2 | List each customer's distinct active months.
Step 3 | k = active month minus cohort month, in months.
Step 4 | Count distinct customers per (cohort, k); divide by the cohort size (k = 0).
@@
@@py
import sys
sys.path.insert(0, DATA)
import prep
import numpy as np, pandas as pd
o, c, p = prep.load_clean(DATA)
con = prep.clean_db(DATA)

q = """
WITH f AS (SELECT customer_id, MIN(substr(order_date,1,7)) AS cohort FROM orders GROUP BY 1),
     a AS (SELECT DISTINCT customer_id, substr(order_date,1,7) AS m FROM orders)
SELECT cohort,
       (CAST(substr(m,1,4) AS INT)*12 + CAST(substr(m,6,2) AS INT)) -
       (CAST(substr(cohort,1,4) AS INT)*12 + CAST(substr(cohort,6,2) AS INT)) AS k,
       COUNT(*) AS n
FROM a JOIN f USING (customer_id) GROUP BY 1, 2"""
sql = pd.DataFrame(con.execute(q).fetchall(), columns=["cohort", "k", "n"]).pivot(index="cohort", columns="k", values="n")

o["m"] = o.order_date.dt.to_period("M")
first = o.groupby("customer_id").m.min().rename("cohort")
x = o.join(first, on="customer_id")
x["k"] = (x.m - x.cohort).apply(lambda v: v.n)
mat = x.groupby(["cohort", "k"]).customer_id.nunique().unstack()
print("SQL matrix equals pandas matrix:", np.array_equal(np.nan_to_num(sql.values), np.nan_to_num(mat.values)))

ret = (mat.div(mat[0], axis=0) * 100).round(0)
print(ret.loc[:, 0:4].head(6).to_string())
print("average month-1 retention, cohorts Jan-Oct:", round(ret.loc[:"2024-10", 1].mean(), 1), "%")
@@
<figure><img src="images/ch04_retention.png" alt="Heatmap of retention percent by first-order cohort and months since first order" loading="lazy"/><figcaption>Retention by cohort. Each row is the customers whose first order in the data fell in that month; each column is how many months later they ordered again.</figcaption></figure>
<p>How to read it: the diagonal edge is the end of the data, not a cliff (later cohorts have had less time). Reading along a row shows how a cohort fades; reading down a column compares cohorts at the same age. A warning: the January cohort is inflated by customers who joined in 2023 and simply made their first order of <em>2024</em> in January, so "first order in the data" is not "first order ever". This is called left censoring, and it is why Chapter 6 defines churn with an explicit observation window.</p>
<h3>Cohorts in Excel and DAX (not run here)</h3>
@@table
Tool | How
Excel | Helper columns in the Orders table: <code>FirstMonth = MINIFS([order_date],[customer_id],[@customer_id])</code> then <code>Cohort = TEXT([@FirstMonth],"yyyy-mm")</code> and <code>Age = DATEDIF([@FirstMonth],[@order_date],"m")</code>. Build a PivotTable with Cohort in Rows, Age in Columns and Distinct Count of customer_id (add the data to the Data Model to get Distinct Count). Show Values As, % of Row Total is wrong for retention; divide each cell by the Age 0 cell.
Power BI | Calculated column on Orders: <code>Cohort = CALCULATE(MIN(Orders[order_date]), ALLEXCEPT(Orders, Orders[customer_id]))</code>; <code>Age = DATEDIFF(Orders[Cohort], Orders[order_date], MONTH)</code>; measure <code>Active = DISTINCTCOUNT(Orders[customer_id])</code>; matrix visual with Cohort month on rows, Age on columns. Retention measure: <code>DIVIDE([Active], CALCULATE([Active], Orders[Age] = 0))</code> inside the matrix row context.
R | <code>orders %&gt;% group_by(customer_id) %&gt;% mutate(cohort = min(month)) %&gt;% group_by(cohort, age) %&gt;% summarise(n = n_distinct(customer_id))</code>
@@
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">A retention heatmap is often the first page of a subscription or retail review. Executives look for two things: whether the color of the first column (month 1) is improving for newer cohorts, and where the sharp fall happens. If month 1 is high but month 2 falls, the fix is in the second order experience, not in acquisition.</div></div>

<h2>4.6 Seeing it: six charts and the design checklist</h2>
<p>A chart is an argument: it should make one comparison easy. The choice of form follows the question, not the other way round.</p>
@@table
Question | Chart | ShopKart example
How does a value change over time? | Line | Revenue by month
Which category is larger? | Horizontal bar (long labels), column (short) | Revenue by category and city
How is a number spread? | Histogram | Delivery minutes
Do two numbers move together? | Scatter | Order hour vs delivery time
Which parts make a whole (only few parts)? | Stacked bar, or avoid pies | Channel mix
Retention or a matrix of two categories | Heatmap | Cohort chart above
@@
<figure><img src="images/ch04_six_charts.png" alt="Six small charts: line of revenue by month, bar of revenue by category, column of revenue by city, histogram of delivery minutes, bar of return rate by category, scatter of order hour against delivery minutes" loading="lazy"/><figcaption>The six standard charts of the ShopKart dashboard, drawn with matplotlib from the cleaned data.</figcaption></figure>
<p>How to read it: chart 1 shows growth to an August peak with a November bump; chart 2 shows Fashion and Electronics ahead; chart 3 shows Bengaluru first; chart 4 has a right-skewed shape (most deliveries near 40 minutes, a tail of slow ones); chart 5 shows Fashion with the highest return rate; chart 6 shows that the evening hours (18 to 21) are slower. These are findings to test in Chapter 5 and exploit in Chapter 6, not conclusions.</p>
<p>The code for chart 2 is five lines in matplotlib. The same chart in other tools:</p>
@@table
Chart | matplotlib (run) | Excel recipe (not run here) | Power BI visual (not run here)
Line | <code>ax.plot(x, y)</code> | Select the monthly PivotTable, Insert, Line | Line chart; Axis: Dates[Month]; Values: [Revenue]
Bar | <code>ax.barh(names, values)</code> | Insert, Bar, sort the PivotTable first | Clustered bar chart; sort by [Revenue]
Column | <code>ax.bar(names, values)</code> | Insert, Column | Clustered column chart
Histogram | <code>ax.hist(x, bins=40)</code> | Insert, Statistic Chart, Histogram; set bin width to 5 | Needs a bin column: right-click the field, New group, Bin size 5; then column chart of Count
Scatter | <code>ax.scatter(x, y, alpha=.4)</code> | Insert, Scatter; two numeric columns | Scatter chart; X, Y and Details fields (limit points for speed)
Heatmap | <code>ax.imshow(matrix)</code> | Conditional Formatting, Color Scales on the retention matrix | Matrix visual with conditional formatting, background color by value
@@
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">The dashboard checklist. (1) One question per chart, stated in the title. (2) Start bars at zero. (3) Sort categories by value, not alphabet. (4) Label axes with units. (5) Few colors, and the same color means the same thing everywhere. (6) Avoid 3-D and dual axes. (7) Put the most important number top left. (8) Check that colors work for color-blind viewers (blue and orange, not red and green). (9) Filter controls (slicers) at the side, not in the middle. (10) Write the takeaway in a sentence.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>The truncated axis.</strong> Wrong: a column chart of return rates starting at 4 percent, which makes 5 percent look like five times 4 percent. Right: bars start at zero. Lines may use a tighter range, but label it clearly.</div></div>

<h2>4.7 Speed and readability: when the tool matters</h2>
<p>All four tools got the same numbers. They differ in speed on larger data, in how the logic reads, and in who can maintain it. To feel the speed, we repeat the category revenue 20 times (400,000 rows) and time three methods. Exact seconds depend on your machine, so we print only which is faster, which is stable.</p>
@@py
import sys, time, sqlite3
sys.path.insert(0, DATA)
import prep
import pandas as pd
o, c, p = prep.load_clean(DATA)
big = pd.concat([o[["category", "revenue"]]] * 20, ignore_index=True)

t = time.perf_counter()
tot = {}
for cat, rev in zip(big["category"], big["revenue"]):
    tot[cat] = tot.get(cat, 0.0) + rev
t_loop = time.perf_counter() - t

t = time.perf_counter()
pdres = big.groupby("category").revenue.sum()
t_pd = time.perf_counter() - t

con = sqlite3.connect(":memory:")
big.to_sql("big", con, index=False)
sres = dict(con.execute("SELECT category, SUM(revenue) FROM big GROUP BY category").fetchall())

print("rows:", len(big))
print("same answer:", all(abs(tot[k] - pdres[k]) < 1 and abs(sres[k] - pdres[k]) < 1 for k in tot))
print("pandas faster than loop:", t_pd < t_loop)
@@
<p>Vectorised pandas beats the Python loop, which has to run Python bytecode 400,000 times. SQLite, a small embedded database, gives the same answer but is not built for raw speed on a single scan like this; its advantages are persistence, indexes and not needing the data in memory, and server warehouses with columnar storage are far faster still. The loop wins on clarity for teaching, and on flexibility when the logic does not fit a table (for example, a state machine across events).</p>
@@table
Criterion | SQL | pandas | Excel | Power BI / DAX
Readability for aggregation | Very high (declarative) | High | High for small data | High once measures exist
Reuse | Views, stored queries | Functions | Copy and paste | Measures reused across visuals
Audit trail | Query text | Code | Weak | Model plus measures
Interactivity | None | Notebook widgets | Slicers, PivotTables | Best (cross-filtering)
Typical ceiling | Billions of rows in a warehouse | Millions in memory | About 1 million rows | Tens of millions compressed
Learning curve | Moderate | Moderate | Gentle | Gentle for visuals, steep for DAX context
@@
<h3>Going deeper: filter context versus row context</h3>
<p>DAX trips up experienced SQL users because a measure is evaluated <em>in the context of each cell</em>. When a visual shows category Fashion, the measure <code>SUM(Orders[revenue])</code> sees only Fashion rows, because the visual applies a filter. <code>CALCULATE</code> changes that filter: <code>CALCULATE([Revenue], ALL(Orders[category]))</code> removes the category filter and returns total revenue, which divided into the cell gives a share: <code>Share = DIVIDE([Revenue], CALCULATE([Revenue], ALL(Orders[category])))</code>. The SQL equivalent is a window over the whole table, <code>SUM(rev) * 1.0 / SUM(SUM(rev)) OVER ()</code>, and the pandas one is <code>g / g.sum()</code>. Same idea, three vocabularies. Let us confirm the numbers:</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep
o, c, p = prep.load_clean(DATA)
con = prep.clean_db(DATA)
sql = con.execute("SELECT category, ROUND(SUM(revenue) * 100.0 / SUM(SUM(revenue)) OVER (), 1) FROM orders GROUP BY category ORDER BY 2 DESC").fetchall()
g = o.groupby("category").revenue.sum()
pdv = (g / g.sum() * 100).round(1).sort_values(ascending=False)
print(sql)
print(pdv.to_dict())
@@

<h2>Chapter recap</h2>
<ul><li>Aggregation is key, measure, function; every tool has the same operation under a different name.</li><li>Always show count and value together (Electronics: few orders, high value).</li><li>Never average averages; divide totals.</li><li>Joins change row counts: check before and after, and make the "one" side unique.</li><li>Window functions keep rows and add running totals, previous values, ranks and moving averages; state the ORDER.</li><li>Cohort retention separates growth by acquisition from loyalty; beware left censoring.</li><li>Pick the chart by the question; start bars at zero; sort bars.</li><li>DAX measures follow filter context; CALCULATE and ALL change it.</li><li>For speed, vectorised pandas and SQL engines beat Python loops; Excel is limited by size.</li></ul>
@@table
Pattern | Meaning
<code>GROUP BY k</code> / <code>groupby(k)</code> / PivotTable rows / visual axis | Grouping key
<code>SUM(x) OVER (ORDER BY d)</code> / <code>cumsum</code> | Running total
<code>LAG(x)</code> / <code>shift(1)</code> | Previous row
<code>COUNT(DISTINCT id)</code> / <code>nunique</code> / <code>DISTINCTCOUNT</code> | Distinct entities
<code>LEFT JOIN ... IS NULL</code> / <code>~isin</code> | Anti-join, rows with no match
Retention(k) = active at k ÷ cohort size | Share of cohort still ordering
@@

<h2>Practice set</h2>
@@qa 4.8
Q: Which category has the highest net revenue, and what share of total revenue is it?
A: ~~cat_rev.index[0]~~ with ~~cat_rev.iloc[0]/cat_rev.sum():.1%~~ of revenue (rupees ~~cat_rev.iloc[0]:,.0f~~).
Q: Which month has the highest revenue and how much is it?
A: Month number ~~month_rev.idxmax()~~ (August), rupees ~~month_rev.max():,.0f~~.
Q: Write the SQL for revenue by city, highest first.
A: <code>SELECT city, SUM(revenue) FROM orders GROUP BY city ORDER BY 2 DESC;</code> Top city: ~~city_rev.index[0]~~.
Q: Write the Excel formula for revenue of category in A2 and the DAX measure for total revenue.
A: Excel <code>=SUMIFS(Orders[revenue],Orders[category],A2)</code>; DAX <code>Revenue = SUM(Orders[revenue])</code>.
Q: Four cities have average order values of 800, 900, 1,000 and 1,100 with 10, 10, 10 and 970 orders. Is the overall average 950?
A: No. Weighted: (8,000 + 9,000 + 10,000 + 1,067,000) ÷ 1,000 = 1,094. The simple mean of averages (950) ignores the weights.
Q: An inner join of orders to customers returns ~~len(o):,~~ rows. How many would a left join return, and why?
A: The same, ~~len(o):,~~, because every order has a customer (consistency check from Chapter 2); a left join would only differ if an order had an unknown customer.
Q: A join doubled revenue. Give two checks that find the cause.
A: Compare row counts before and after; check that the right table's key is unique (<code>HAVING COUNT(*) &gt; 1</code>, or <code>validate="m:1"</code>).
Q: What is the difference between <code>ROW_NUMBER()</code> and <code>RANK()</code>?
A: ROW_NUMBER gives a unique number even for ties; RANK gives ties the same rank and then skips numbers (1, 2, 2, 4).
Q: For a 7-day moving average, what should the first six days show and why?
A: Either missing values (strict 7 days required) or averages over the available days (<code>min_periods=1</code>); state which one you chose.
Q: Compute month-1 retention for a cohort of 250 customers where 100 order again in the next month.
A: 100 ÷ 250 = 40 percent.
Q: Why is the retention of the January cohort in the heatmap misleading?
A: Its members include customers who joined in 2023; their first 2024 order is not their first order ever (left censoring), so the cohort is a mix of old and new customers.
Q: Find the bug: a column chart of return rate by category with y axis starting at 5 percent.
A: The truncated axis exaggerates differences; start the bars at zero.
Q: Interview style: "A DAX measure shows blank for last year in Power BI. What do you check?"
A: Whether a complete date table exists and is related to the fact table, whether it is marked as a date table, and whether the measure uses a time-intelligence function over that table's Date column and not over the fact table's date.
@@

<h2>Prompt pack</h2>
@@prompt
You are my patient, practical professor. I am a working professional moving into data roles. Teach me analytical SQL and pandas side by side using an online retail orders table: group by, joins, window functions, cohorts and retention. Give me one task at a time, ask for the SQL and the pandas version, check that both give the same result, and explain any difference.
@@
@@prompt
Act as a business intelligence lead reviewing my dashboard design. Here is the list of charts and the question each answers: [paste]. Apply a ten-point checklist (one question per chart, zero baseline, sorting, units, color use, no 3-D, key number placement, color-blind safety, slicer placement, written takeaway) and rewrite titles so each states its finding.
@@
@@prompt
Run a mock interview for a BI or data analyst role. Ask me, one at a time, to explain with examples: fan-out in joins, window functions versus group by, cohort retention, DAX filter context versus SQL, and when to use Excel, SQL or Power BI. Grade each answer and give a final summary.
@@
