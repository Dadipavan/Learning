<p>It is Monday, 9:40. Meera, head of growth at ShopKart, a quick-commerce shop that delivers groceries, electronics, fashion, home goods and beauty products in five Indian cities, forwards you an email from the CEO: "Orders are up but I do not feel richer. Are deliveries getting late? Are customers leaving? What should we do next quarter?" Attached is a folder: a 1.7 MB file called <code>orders.csv</code>, another called <code>customers.csv</code>, a small <code>products.csv</code> and a database file. No instructions. No definitions. A meeting at 15:00.</p>
<p>What you do in the next few hours decides everything. Do you open Excel, run a query, write a notebook? Do you clean first, or explore first? Do you build a model before you know what "late" means? Most beginners jump to a tool. Experts first fix the question, then walk a path that is almost always the same: <strong>frame</strong> the problem, <strong>ingest and store</strong> the data, <strong>clean and profile</strong> it, <strong>analyse</strong> it, <strong>test</strong> ideas with statistics, <strong>model</strong> the future with machine learning, add <strong>deep learning and GenAI</strong> where they truly help, and finally <strong>deliver and monitor</strong> the result.</p>
<p>This document takes you along that path, once, end to end, on <em>one</em> dataset. Every stage is a chapter. In every stage we show the process as numbered steps, the tools that can do it (SQL, pandas, plain Python, Excel, Power BI and sometimes R, side by side), the thing you must produce, and what goes wrong. After this first chapter you will be able to turn a vague email into ten measurable questions, load the data in every common tool, and know the expected answers before you start, so that you can tell when a tool or a person is wrong.</p>

<h2>1.1 The path from raw data to decisions</h2>
<p>Think of cooking for a dinner party. You decide the menu (framing), buy and store ingredients (data engineering), wash and trim them (cleaning), taste and combine (analysis), check a recipe change with a fair taste test (statistics), cook tomorrow's menu from patterns of what guests ate (machine learning), try an exotic technique if it adds something (deep learning, GenAI), and finally serve, and watch whether guests keep coming back (operations and monitoring). Nobody starts with the exotic technique. Nobody serves unwashed vegetables.</p>
@@table
Stage | Chapter | Main question | What you produce | Main roles
1 Frame | 1 | What decision are we helping, and how will we know we are right? | Question list, metric definitions, data dictionary | Everyone, analyst leads
2 Engineer | 2 | Where does the data live, and can we load it again tomorrow? | Tables, schema, quality checks, pipeline script | Data engineer
3 Clean | 3 | Can we trust the numbers? | Cleaned tables and a cleaning log | Analyst, data engineer
4 Analyse | 4 | What happened, where and for whom? | Aggregates, cohorts, charts, dashboard | Analyst
5 Test | 5 | Is the difference real, and what will happen next month? | Intervals, test results, forecasts | Analyst, data scientist
6 Model | 6 | Who will be late, who will leave? | Validated model, metrics, cost-based threshold | Data scientist
7 Deep and GenAI | 7 | Do richer models or language models add value? | Neural net, text search, QA prototype | ML and GenAI engineers
8 Deliver | 8 | How do we ship it and keep it healthy? | Packaged model, monitoring, decision memo | ML engineer, analyst
@@
<div class="callout green"><div class="lab">BASIC EXPLANATION</div><div class="txt">The data-analysis path is the ordered set of stages that takes raw data to a decision: frame the question, get and clean the data, analyse it, check it, model it and act on it. It is used to plan work so that each stage has a clear output.</div></div>
<div class="callout blue"><div class="lab">INTUITION</div><div class="txt">The stages are a loop, not a line. A surprise in Stage 4 (a city with 3 percent returns and another with 30) sends you back to Stage 3 (is that a spelling problem?). Good teams expect to revisit earlier stages and keep notes so that a revisit costs minutes, not days.</div></div>

<h3>Going deeper: why one dataset?</h3>
<p>Real projects do not give you a new dataset at each stage. They give you one messy source, and the quality of every later stage depends on choices made in earlier ones: how you handled the duplicates changes revenue, which changes the forecast, which changes the model's training labels. Using a single dataset throughout lets you see these dependencies. When you reach Chapter 6 and a feature is suspiciously good, you will already know the dataset well enough to ask why.</p>

<h2>1.2 From an email to ten measurable questions</h2>
<p>"Orders are up but I do not feel richer" is not a question a computer can answer. A measurable question names a <strong>metric</strong> (a number computed in a defined way), a <strong>slice</strong> (period, city, segment) and a <strong>comparison</strong> (against what). The process has four steps.</p>
<ol><li><strong>Restate the decision.</strong> Here: where to spend next quarter's budget (delivery capacity, discounts or retention).</li><li><strong>List candidate metrics.</strong> Revenue, order count, average order value, return rate, late rate, repeat rate.</li><li><strong>Define each metric in one sentence</strong> with its filter, so two people compute the same value.</li><li><strong>Write the expected shape of the answer</strong> (a number, a table, a chart, a yes or no).</li></ol>
@@table
# | Business question | Metric definition | Answered in
Q1 | How big was 2024? | Number of distinct orders after removing duplicates; net revenue = quantity × unit price × (1 − discount) for delivered orders only | Ch 1, 3, 4
Q2 | When do we sell most? | Net revenue by month | Ch 4
Q3 | Which category earns most? | Net revenue by category | Ch 4
Q4 | Which city earns most? | Net revenue by standardised city | Ch 3, 4
Q5 | How many orders come back? | Returned orders ÷ all orders | Ch 4
Q6 | Are deliveries late? | Late = delivery minutes &gt; promised minutes; rate over orders that have both numbers | Ch 4, 6
Q7 | How much does an order bring? | Average net value of delivered orders | Ch 4
Q8 | Do customers come back? | Share of customers with at least 2 orders; month-1 and month-3 retention | Ch 4
Q9 | Do discounts cause more sales? | Difference in units per order between discount and no-discount, with an interval | Ch 5
Q10 | Who is about to leave, and which order will be late? | Predicted probability, evaluated on future data | Ch 6, 7, 8
@@
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">A metric without a definition is an argument waiting to happen. Write definitions down before computing. Q1 alone has three plausible answers (all rows, distinct orders, delivered orders only) and each leads to a different revenue.</div></div>

<h2>1.3 The dataset: dictionary and structure</h2>
<p>ShopKart has three tables. The data was generated by a script (<code>tools/ways/make_data.py</code>, a fixed random seed) so that every reader gets identical files, but it contains the faults of real data on purpose: spelling variants, missing values, duplicate rows, impossible values and extreme outliers. Nothing in it is real customer data.</p>
@@table
Table | Column | Meaning | Type | Known quirks
orders | order_id | Unique id of an order line | integer | 150 ids appear twice (duplicates)
orders | customer_id | Who ordered, joins to customers | integer | none
orders | order_date | Date of order, 2024-01-01 to 2024-12-31 | date text | read as text in some tools
orders | order_hour | Hour of day 0 to 23 | integer | none
orders | city | Delivery city | text | spelling variants, trailing spaces, 120 missing
orders | channel | App, Web or Store pickup | text | about 60 missing
orders | category, product | What was bought; product joins to products | text | none
orders | quantity | Units | integer | 5 absurd values (40, 60, 99)
orders | unit_price | Price per unit in rupees | decimal | 90 missing
orders | discount | Fraction taken off, 0 to 0.2 | decimal | none
orders | status | delivered, returned or cancelled | text | none
orders | promised_minutes | Delivery promise, 45 or 60 | decimal | empty for store pickup
orders | delivery_minutes | Actual minutes to deliver | decimal | empty if cancelled or pickup; negative and extreme values
customers | customer_id, signup_date, segment, age | Who the customer is | mixed | segment Regular, Premium or Student; about 4 percent of ages missing
products | product_id, product, category, list_price, unit_cost, description | Catalogue | mixed | 32 products, used for text work in Ch 7
@@
<p>The files live in <code>study/ways/data/</code>: <code>orders.csv</code>, <code>customers.csv</code>, <code>products.csv</code> and <code>shopkart.db</code> (the same three tables in SQLite). In every code block of this document the first line is <code>DATA = "..."</code>, an absolute path to that folder. Change it if you move the files. The file <code>prep.py</code> in the same folder contains the cleaning we develop in Chapter 3, so later chapters can reuse it without repeating 15 lines in every block.</p>

<h2>1.4 Loading the data in every tool</h2>
<p>Loading looks trivial and is where many silent errors begin: a date read as text, an id read as a number with a decimal point, a leading zero lost, an encoding wrong. For each tool we show the exact action, then compare the first answer: how many rows?</p>
<p class="problem"><span class="pl">Problem 1.4.1</span> Load <code>orders.csv</code> and report the number of rows and columns, and the date range, with pandas, with plain Python, and with SQLite.</p>
@@steps
Idea | Three tools must agree before we trust any of them. The raw file has one header line plus one line per order row.
pandas | <code>read_csv</code> with <code>parse_dates</code> turns the date text into real dates.
Plain Python | the <code>csv</code> module reads each line as strings; you convert yourself.
SQLite | the database already stores the table; <code>COUNT(*)</code> counts rows.
@@
@@py
import csv, sqlite3
import pandas as pd

# 1. pandas
df = pd.read_csv(DATA + "orders.csv", parse_dates=["order_date"])
print("pandas :", df.shape, df.order_date.min().date(), df.order_date.max().date())

# 2. plain Python
with open(DATA + "orders.csv", newline="") as f:
    rows = list(csv.DictReader(f))
dates = [r["order_date"] for r in rows]
print("python :", (len(rows), len(rows[0])), min(dates), max(dates))

# 3. SQL (SQLite)
con = sqlite3.connect(DATA + "shopkart.db")
print("sql    :", con.execute("SELECT COUNT(*), MIN(order_date), MAX(order_date) FROM orders").fetchone())
@@
<p>All three say 20,150 rows. ISO dates (year-month-day) sort correctly even as text, which is why the plain Python and SQL versions get the right minimum and maximum without conversion. This is also why you should always store dates in ISO form.</p>
<h3>The same load in Excel, Power BI and R (not run here)</h3>
@@table
Tool | Steps or code | Watch out for
Excel | Data tab, Get Data, From Text/CSV, pick <code>orders.csv</code>, check that the detected delimiter is a comma, click Transform Data if you need to fix types, then Load. Keep it as a Table (Ctrl+T) and name it <code>Orders</code>. | Opening the CSV by double-click lets Excel guess types and can turn dates into the local format. A sheet holds at most 1,048,576 rows, plenty here.
Power BI | Home, Get data, Text/CSV, orders.csv, Transform Data. In Power Query set <code>order_date</code> to Date, <code>order_id</code> and <code>customer_id</code> to Whole Number, prices to Fixed decimal. Close and Apply. | Type detection samples only the first 200 rows by default; set it to the entire dataset for safety.
R | <code>orders &lt;- readr::read_csv(file.path(DATA, "orders.csv"))</code> then <code>dim(orders)</code> | readr guesses types from the first 1,000 rows; give <code>col_types</code> to be sure.
@@
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Trusting the guessed types.</strong> Wrong: opening <code>orders.csv</code> in Excel, seeing 2024-03-04 turn into 04-03-2024 and then reading it as 4 March in one place and 3 April in another. Right: load through the import wizard or Power Query and set the date type explicitly. Rule of thumb: after every load, print the types and the min and max of every date.</div></div>

<h2>1.5 A first profile in two tools</h2>
<p>A profile is a one-page health check: how many rows, how many missing values per column, how many distinct values in key columns, what ranges numbers have. It costs minutes and prevents hours of confusion. The full cleaning is Chapter 3; here we only look.</p>
@@py
import pandas as pd
df = pd.read_csv(DATA + "orders.csv", parse_dates=["order_date"])
print("rows", len(df), "| distinct order_id", df.order_id.nunique(), "| distinct customers", df.customer_id.nunique())
print("fully duplicated rows:", df.duplicated().sum())
print("missing per column:")
print(df.isna().sum()[lambda s: s > 0].to_string())
print("distinct city spellings:", df.city.nunique())
print(df[["quantity", "unit_price", "delivery_minutes"]].describe().loc[["min", "50%", "max"]].round(1).to_string())
@@
<p>The same profile in SQL asks the database to count for us. SQLite has no built-in <code>describe</code>, so we write each statistic, which is more typing and also makes each definition explicit.</p>
@@py
import sqlite3
con = sqlite3.connect(DATA + "shopkart.db")
q = """
SELECT COUNT(*) AS n_rows,
       COUNT(DISTINCT order_id) AS n_order_ids,
       COUNT(DISTINCT customer_id) AS n_customers,
       SUM(city IS NULL) AS city_missing,
       SUM(unit_price IS NULL) AS price_missing,
       SUM(channel IS NULL) AS channel_missing,
       COUNT(DISTINCT city) AS city_spellings,
       MIN(quantity) AS qmin, MAX(quantity) AS qmax,
       MIN(delivery_minutes) AS dmin, MAX(delivery_minutes) AS dmax
FROM orders"""
cur = con.execute(q)
for name, val in zip([d[0] for d in cur.description], cur.fetchone()):
    print(f"{name:18s}{val}")
@@
<p>Both profiles agree: 20,150 rows but only 20,000 distinct order ids (so 150 duplicates), 120 missing cities, 90 missing prices, about 60 missing channels, many city spellings, quantities up to 99 and delivery times from negative to 2,900 minutes. Notice that pandas says "unique values" and SQL says <code>COUNT(DISTINCT)</code>; both ignore missing values, a fact that matters for Chapter 3.</p>
<div class="callout cream"><div class="lab">REAL JOB</div><div class="txt">Many teams save the profile as the first page of the project notebook and rerun it whenever new data arrives. A change in the profile (a new city spelling, a jump in missing prices) is the cheapest alarm you can have. We build it into a pipeline in Chapter 2.</div></div>

<h2>1.6 The expected answers: raw versus cleaned</h2>
<p>Before analysis, write down what each tool <em>should</em> return. You will check this table again in Chapters 3 and 4, in four tools. Notice how far the naive answer is from the cleaned one: this is the reason the next two chapters exist.</p>
@@py
import sys
sys.path.insert(0, DATA)
import prep
raw, cust, prods = prep.load_raw(DATA)
o, cust, prods = prep.load_clean(DATA)
naive_rev = (raw.quantity * raw.unit_price * (1 - raw.discount)).sum()
print(f"raw rows            {len(raw):>12,}")
print(f"clean orders        {len(o):>12,}")
print(f"naive revenue       {naive_rev:>12,.0f}   (all rows, no cleaning, missing prices skipped)")
print(f"clean net revenue   {o.revenue.sum():>12,.0f}   (delivered only)")
print(f"avg order value     {o[o.status=='delivered'].net.mean():>12,.1f}")
print(f"return rate         {(o.status=='returned').mean():>12.4f}")
print(f"late rate           {o.late.mean():>12.4f}   ({o.late.notna().sum():,} orders with both times)")
print(f"repeat customers    {(o.groupby('customer_id').size() >= 2).mean():>12.4f}")
@@
<p>Naive revenue is about ~~(raw.quantity*raw.unit_price*(1-raw.discount)).sum()/o.revenue.sum()::.2f~~ times the clean value, an overstatement driven by returned and cancelled orders, duplicates and the absurd quantities. Which one the CEO should see is a definition question (Section 1.2), not a computing question.</p>
@@table
Question | Clean answer (pandas) | How the other tools get it
Q1 orders, revenue | ~~n_orders::,~~ orders; rupees ~~rev_total::,.0f~~ | SQL <code>SUM(revenue)</code> on cleaned table; Excel <code>SUMIFS</code>; DAX <code>SUMX</code>
Q2 best month | month ~~month_rev.idxmax()~~ (rupees ~~month_rev.max()::,.0f~~) | SQL <code>GROUP BY substr(order_date,1,7)</code>; PivotTable by month
Q3 top category | ~~cat_rev.index[0]~~ (~~cat_rev.iloc[0]/cat_rev.sum()::.1%~~ of revenue) | same pattern, group by category
Q4 top city | ~~city_rev.index[0]~~ (~~city_rev.iloc[0]/city_rev.sum()::.1%~~) | requires cleaned city names first
Q5 return rate | ~~ret_rate::.1%~~ | <code>AVG(status='returned')</code> in SQL; <code>COUNTIFS</code> ÷ <code>COUNTA</code>
Q6 late rate | ~~late_rate::.1%~~ | <code>AVG(late)</code> ignoring missing
Q7 average order | rupees ~~aov::,.0f~~ | <code>AVERAGEIFS</code>; DAX <code>AVERAGEX</code>
Q8 repeat share | ~~repeat_share::.1%~~ of customers who ordered | SQL <code>GROUP BY customer_id HAVING COUNT(*)&gt;=2</code>
@@
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Dividing by the wrong denominator.</strong> Wrong: late rate = late orders ÷ all orders, which counts store pickups and cancellations as "on time". Right: divide by the orders that have both a promise and a delivery time. The same data gives ~~o.late.sum()/len(o)::.1%~~ the first way and ~~late_rate::.1%~~ the second.</div></div>

@@green
Write the expected answers <em>before</em> running the query, even roughly ("about 17 million"). A result that differs from your guess by a factor of two is almost always a bug or a definition problem, not a discovery.
@@
<h2>1.7 Ethics, privacy and scope</h2>
<p>Every stage touches people. A customer id looks harmless until it is joined with age, city and order times; then it can single out an individual. Four habits protect people and you.</p>
<ol><li><strong>Minimise.</strong> Take only the columns you need. We will never need names or addresses, and the dataset has none.</li><li><strong>Pseudonymise.</strong> Keep ids, not names. Store the lookup table elsewhere under access control.</li><li><strong>Check fairness before deploying.</strong> A model that predicts late deliveries per city may send worse service to the cities it predicts as slow. Compare errors across groups (Chapter 6).</li><li><strong>Document limits.</strong> State what the data cannot answer: one year, five cities, no competitor data, no reasons for returns.</li></ol>
<h3>Going deeper: aggregate before you share</h3>
<p>A table with fewer than a handful of people in a cell (for example, Student customers in Pune who ordered Perfume on one date) can re-identify someone. A simple rule used by many organisations is a minimum group size (often 5 to 10) before a number leaves the team. It is a policy choice, not a law of nature; ask your data protection officer for the actual threshold in your company.</p>

<h2>1.8 Choosing tools: a first map</h2>
<p>The same Q1 to Q8 can be answered by any tool in the table. The tool changes who can do it, how fast, and how repeatable it is.</p>
@@table
Tool | Strength | Weakness | Best when
SQL | Fast on large tables, one declarative statement, lives next to the data | Awkward for statistics and charts | The data already sits in a database
pandas | Flexible, scriptable, links to statistics and ML | Memory bound on one machine | Exploration, cleaning, modelling
Plain Python | No dependencies, teaches the logic | Slow and verbose for tables | Tiny jobs, logic that tables cannot express
Excel | Everyone has it; instant visual feedback | Hidden manual steps, hard to audit | Small data, quick checks, stakeholder hand-offs
Power BI | Interactive dashboards, a governed data model | Learning DAX; less suited to modelling | Recurring reports for many viewers
R | Statistics and graphics are first class | Smaller engineering ecosystem | Statistical analysis, academic work
@@
<p>Chapter 4 gives a full decision matrix; for now remember that a good analyst can read all of these and writes in two or three of them.</p>

<h2>Chapter recap</h2>
<ul><li>The path is frame, engineer, clean, analyse, test, model, deep and GenAI, deliver; expect loops.</li><li>Turn a vague email into metrics with a definition, a slice and a comparison.</li><li>ShopKart has orders (~~len(raw)::,~~ raw rows), customers (~~len(c)::,~~) and products (~~len(p)~~), with deliberate quirks.</li><li>Always load with explicit types and print the min and max of dates.</li><li>A profile (rows, distinct keys, missing values, ranges) takes minutes and finds most data problems.</li><li>pandas, plain Python and SQL agree on row counts; if they ever disagree, a type or a definition differs.</li><li>Naive and cleaned revenue differ by a large factor; definitions decide which is right.</li><li>Choose the denominator of every rate on purpose.</li><li>Minimise, pseudonymise, check fairness and document limits.</li></ul>
@@table
Pattern | Meaning
Metric = definition + slice + comparison | A measurable question
<code>COUNT(DISTINCT id)</code> vs <code>len(df)</code> | Distinct entities vs rows; difference shows duplicates
Rate = events ÷ eligible cases | Choose the eligible set explicitly
Profile first | Rows, keys, missing, ranges, types
@@

<h2>Practice set</h2>
@@qa 1.9
Q: Name the eight stages of the path and the chapter where each is covered.
A: Frame (1), engineer (2), clean (3), analyse (4), test (5), model (6), deep learning and GenAI (7), deliver (8).
Q: Rewrite "Are customers leaving?" as a measurable question with a metric, a slice and a comparison.
A: "What share of customers who ordered in Q3 2024 placed no order in the following 90 days, and is it higher for Student than Regular customers?" Metric: churn share; slice: Q3 customers; comparison: Student versus Regular.
Q: How many orders (rows) does the raw file have, and how many distinct order ids?
A: ~~len(raw)::,~~ rows and ~~raw.order_id.nunique()::,~~ distinct ids, so ~~len(raw)-raw.order_id.nunique()~~ duplicates.
Q: Give the formula for net revenue of one order line and compute it for 3 units at 250 rupees with a 10 percent discount.
A: quantity × unit price × (1 − discount) = 3 × 250 × 0.9 = 675 rupees.
Q: In SQL, which function counts rows and which counts distinct values, and how do both treat NULL?
A: <code>COUNT(*)</code> counts rows including NULLs; <code>COUNT(col)</code> skips NULLs; <code>COUNT(DISTINCT col)</code> counts distinct non-NULL values.
Q: Why do ISO dates (2024-03-04) sort correctly as plain text?
A: The most significant part (year) comes first, then month, then day, all zero padded, so alphabetical order equals chronological order.
Q: What are three ways the naive revenue of the raw file is wrong?
A: It includes duplicate rows, returned and cancelled orders (depending on definition), and the absurd quantities (40, 60, 99); rows with missing prices contribute nothing.
Q: Late rate is ~~late_rate::.1%~~ over ~~o.late.notna().sum()::,~~ orders. How many late orders is that?
A: ~~int(o.late.sum())::,~~ late orders (rate × count, checked against the data).
Q: Which two columns of the orders table cannot be used to judge lateness for a store pickup order, and why?
A: promised_minutes and delivery_minutes are empty, because nothing is delivered.
Q: Find the bug: "return rate = returned rows ÷ distinct customers".
A: The numerator counts orders and the denominator counts people; units differ. Use returned orders ÷ all orders.
Q: List three columns that together could identify a person and say how you would reduce the risk.
A: For example customer_id with age and city. Keep ids pseudonymous, bin age into ranges, and suppress cells with very few people.
Q: Excel opens the CSV and shows 4.3E+05 in the order_id column. What went wrong and how do you fix it?
A: Excel guessed a number format for a wide numeric id and displays scientific notation. Import through Get Data, set the column to Whole Number or Text, widen the column and apply the Number format with no decimals.
Q: Interview style: "Your dashboard shows revenue of X and finance says Y. What do you do?"
A: Compare definitions first (gross or net, delivered only, time zone, duplicates), then compare row counts, then reconcile a single day. Document the agreed definition.
@@

<h2>Prompt pack</h2>
@@prompt
You are my patient, practical professor. I am a working professional moving into data roles. Quiz me, one question at a time, on framing an analytics problem: turning a vague business email into measurable questions with a metric definition, a slice and a comparison. Use an online retail example (orders, customers, deliveries, returns). After each answer tell me what was good, what was missing and give a harder follow-up. Do 8 questions and finish with a score.
@@
@@prompt
Act as a senior analyst reviewing my work. Here are my ten business questions and metric definitions: [paste them]. Check each for ambiguity (denominator, filter, period), point out where two people could compute different numbers, and suggest a sharper wording. Then list five data quality checks I should run before trusting the answers.
@@
@@prompt
Run a mock interview for a junior data analyst role. Start with: "Your CEO says orders are up but revenue feels flat. How do you investigate?" Ask follow-ups one at a time about definitions, duplicates, returns, discounts and the choice of tool (SQL, pandas, Excel, Power BI). Grade my answers at the end and tell me what a strong answer would add.
@@
