<p>Priya, an analyst at ShopKart, builds a revenue-by-city chart for the Monday meeting. It shows eighteen bars. Bengaluru appears four times (Bengaluru, bangalore, "Bangalore " with a trailing space, BENGALURU), Mumbai three, and a mysterious bar called Bombay. Her manager asks which city is biggest, and the honest answer is "none of these bars is a city". Priya's chart is not wrong because her tool is weak. It is wrong because nobody cleaned the data, and every tool, from Excel to R, would draw the same eighteen bars.</p>
<p>Cleaning is the stage where most of the real work in analytics happens, and the stage where most hidden errors enter. In this chapter you will learn a repeatable process, apply it to each fault planted in ShopKart (duplicates, spellings, missing values, outliers, types), and do each fix in several tools with the <em>same</em> result. You will end with a cleaning log, a table of which tool suits which cleaning job, and the exact effect of cleaning on the business answers from Chapter 1.</p>

<h2>3.1 A cleaning process you can defend</h2>
<p>Cleaning is a set of decisions about the truth, so every step should be justified and recorded. Use the same five moves every time.</p>
<ol><li><strong>Detect.</strong> Find the problem with a count (how many rows?).</li><li><strong>Decide.</strong> Choose a rule: drop, fix, fill, flag or leave. Write the reason.</li><li><strong>Act.</strong> Apply the rule in code or a recorded query step, never by hand-editing cells.</li><li><strong>Verify.</strong> Recount: the problem should be gone and nothing else should change.</li><li><strong>Log.</strong> Record rule, rows affected and effect on key metrics.</li></ol>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Never overwrite the raw data and never fix by hand. A cleaning step that is code (a SQL view, a pandas function, a Power Query step) can be reread, reviewed and rerun on tomorrow's file. A hand-edited cell cannot.</div></div>
<p>Our rules, in the order they run, are the ones inside <code>prep.py</code>: drop exact duplicate rows; standardise city; label missing channel as "Unknown"; drop absurd quantities; fill a missing price from the product catalogue; set impossible delivery times to missing; then add revenue and lateness columns. The next sections justify each.</p>

<h2>3.2 Duplicates</h2>
<p>A duplicate is the same real-world event recorded more than once, often by a retried upload. Exact duplicates (every column equal) are safe to drop. Partial duplicates (same id, different status) need a rule such as "keep the latest". ShopKart has 150 exact duplicates.</p>
<p class="problem"><span class="pl">Problem 3.2.1</span> Count and remove exact duplicates with pandas, SQL and plain Python, and confirm all three agree.</p>
@@steps
Detect | Rows minus distinct rows.
pandas | <code>df.duplicated().sum()</code> and <code>drop_duplicates()</code>.
SQL | <code>SELECT DISTINCT *</code> returns unique rows; compare <code>COUNT(*)</code> with the count of the distinct set.
Python | Keep a <code>set</code> of tuples already seen.
@@
@@py
import sqlite3, csv
import pandas as pd

df = pd.read_csv(DATA + "orders.csv")
print("pandas :", df.duplicated().sum(), "duplicates ->", len(df.drop_duplicates()), "rows")

con = sqlite3.connect(DATA + "shopkart.db")
n_all = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
n_distinct = con.execute("SELECT COUNT(*) FROM (SELECT DISTINCT * FROM orders)").fetchone()[0]
print("sql    :", n_all - n_distinct, "duplicates ->", n_distinct, "rows")

seen, kept, n_read = set(), [], 0
with open(DATA + "orders.csv", newline="") as f:
    next(f)                       # skip the header line
    for row in csv.reader(f):
        n_read += 1
        t = tuple(row)
        if t not in seen:
            seen.add(t)
            kept.append(t)
print("python :", n_read - len(kept), "duplicates ->", len(kept), "rows")
@@
<p>The plain Python version shows what the other tools do for you: it remembers every row seen in a <code>set</code> (a collection with instant membership tests) and keeps a row only the first time. Notice that the duplicate count is computed (rows read minus rows kept), never typed in: a habit worth keeping.</p>
<h3>Duplicates in Excel, Power BI and R (not run here)</h3>
@@table
Tool | Recipe | Notes
Excel | Select the table, Data tab, Remove Duplicates, tick all columns. Or count first: add a helper column <code>=COUNTIFS([order_id],[@order_id])</code> and filter values above 1. | Remove Duplicates keeps the first occurrence and deletes the rest immediately: save a copy first.
Power Query | Select all columns, Home, Remove Rows, Remove Duplicates (M step <code>Table.Distinct(Source)</code>). | Recorded as a step, so it reruns on refresh.
DAX | Rarely in the model; to count: <code>Dup = COUNTROWS(Orders) - COUNTROWS(DISTINCT(Orders))</code> | DISTINCT over a whole table returns unique rows.
R | <code>orders %&gt;% dplyr::distinct()</code> and <code>sum(duplicated(orders))</code> | Same meaning as pandas.
@@
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Dropping duplicates on the wrong columns.</strong> Wrong: <code>drop_duplicates(subset=["customer_id", "product"])</code> because "that is what a duplicate looks like". It deletes genuine repeat purchases and shrinks revenue. Right: drop duplicates on the full row, or on the true key (<code>order_id</code>) after checking that duplicated ids really carry identical values.</div></div>

<h2>3.3 Inconsistent text: the city spellings</h2>
<p>Text typed by people or collected from several systems drifts: case, spaces, old names (Bombay, Madras), aliases (New Delhi). The process: list the distinct values with counts, build a mapping to canonical names, apply it, and check the output has only canonical values plus missing.</p>
@@py
import pandas as pd
df = pd.read_csv(DATA + "orders.csv")
print(df.city.value_counts(dropna=False).to_string())
@@
<p>Eighteen distinct values hide five cities. The fix has two parts: normalise (trim spaces, lowercase) which removes most variants, then map the remaining aliases explicitly. Mapping is better than clever fuzzy matching here because the list is short and a wrong guess is worse than an unmapped value.</p>
@@py
import pandas as pd
import sqlite3
df = pd.read_csv(DATA + "orders.csv")
alias = {"bangalore": "Bengaluru", "bengaluru": "Bengaluru", "mumbai": "Mumbai", "bombay": "Mumbai",
         "delhi": "Delhi", "new delhi": "Delhi", "chennai": "Chennai", "madras": "Chennai", "pune": "Pune"}

# pandas
fixed = df.city.str.strip().str.lower().map(alias)
print("pandas:", fixed.value_counts(dropna=False).to_dict())

# SQL: same idea with lower, trim and CASE
con = sqlite3.connect(DATA + "shopkart.db")
q = """
SELECT CASE LOWER(TRIM(city))
         WHEN 'bangalore' THEN 'Bengaluru' WHEN 'bengaluru' THEN 'Bengaluru'
         WHEN 'mumbai' THEN 'Mumbai' WHEN 'bombay' THEN 'Mumbai'
         WHEN 'delhi' THEN 'Delhi' WHEN 'new delhi' THEN 'Delhi'
         WHEN 'chennai' THEN 'Chennai' WHEN 'madras' THEN 'Chennai'
         WHEN 'pune' THEN 'Pune' END AS city_clean, COUNT(*) AS n
FROM orders GROUP BY 1 ORDER BY n DESC"""
print("sql   :", {str(k): v for k, v in con.execute(q).fetchall()})
@@
<p>Both give the same counts (the None entry is the 120 orders with no city, which is a missing value, handled in the next section, not a spelling problem). Notice what <code>.map(alias)</code> does with an unknown value: it returns missing. That is useful, because it makes a new, unexpected spelling visible as a rise in missing values, instead of silently passing through.</p>
<h3>Spellings in Excel, Power BI and R (not run here)</h3>
@@table
Tool | Recipe
Excel formula | <code>=XLOOKUP(LOWER(TRIM([@city])), Alias[key], Alias[city], "")</code> with a small Alias table on another sheet; or <code>=PROPER(TRIM(A2))</code> for a first pass (it cannot fix Bombay)
Excel quick fix | Home, Find and Replace for each variant (fast, but manual and unrecorded)
Power Query | Transform, Format, Trim, then Format, lowercase; then Merge Queries with the Alias table (Left Outer), expand the canonical column. Or Replace Values in the column, one rule per alias.
DAX | A calculated column <code>City Clean = SWITCH(LOWER(TRIM(Orders[city])), "bangalore", "Bengaluru", "bengaluru", "Bengaluru", "bombay", "Mumbai", "mumbai", "Mumbai", BLANK())</code> (extend with the other aliases)
R | <code>dplyr::mutate(city = recode(tolower(trimws(city)), bangalore = "Bengaluru", bombay = "Mumbai"))</code>
@@
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Cleaning the display, not the data.</strong> Wrong: fixing the labels on the chart (renaming the axis) while the underlying column still holds four spellings; the next chart repeats the problem and a join on city silently drops rows. Right: fix the column once, upstream, and let every chart inherit it.</div></div>

<h2>3.4 Missing values</h2>
<p>A missing value is not one problem but several. The right action depends on <em>why</em> it is missing.</p>
@@table
Kind | Meaning | ShopKart example | Reasonable action
Not applicable | The value cannot exist | delivery_minutes for a store pickup or a cancelled order | Leave missing; it is correct information
Lookup available | Another table knows the value | unit_price missing, product catalogue has list_price | Fill from the lookup
Random error | Lost by a faulty system | channel, city | Label Unknown (categorical) or drop if few
Informative | Missingness itself carries meaning | age missing for some customers | Fill with the median and add a flag column
@@
<p class="problem"><span class="pl">Problem 3.4.1</span> Fill the 90 missing unit prices from the products table in pandas and in SQL, and report the revenue that those rows add.</p>
@@steps
Idea | Each order names a product; the catalogue lists its price. Join and take the first non-missing value.
pandas | map product to list_price, then <code>fillna</code>.
SQL | <code>LEFT JOIN products</code> and <code>COALESCE(o.unit_price, p.list_price)</code>.
Check | Both fill the same rows and the same total.
@@
@@py
import sqlite3, pandas as pd
o = pd.read_csv(DATA + "orders.csv").drop_duplicates()
p = pd.read_csv(DATA + "products.csv")
missing = o.unit_price.isna()
filled = o.unit_price.fillna(o["product"].map(p.set_index("product")["list_price"]))
print("pandas: rows filled", missing.sum(), "| still missing", filled.isna().sum(),
      "| gross value of those rows", round((o.quantity * filled)[missing & (o.quantity <= 20)].sum()))

con = sqlite3.connect(DATA + "shopkart.db")
r = con.execute("""
  SELECT COUNT(*), SUM(COALESCE(o.unit_price, p.list_price) IS NULL), ROUND(SUM(o.quantity * p.list_price), 0)
  FROM (SELECT DISTINCT * FROM orders) o JOIN products p ON p.product = o.product
  WHERE o.unit_price IS NULL AND o.quantity <= 20""").fetchone()
print("sql   : rows filled", r[0], "| still missing", r[1], "| gross value of those rows", int(r[2]))
@@
<p>Both agree. A catalogue price is exact when prices never change; if they did, you would look the price up by date. That is an assumption, and a good cleaner writes it down.</p>
<p><strong>Filling with a statistic.</strong> When there is no lookup, the usual fills are the mean, the median or a group median. The median is safer because outliers do not move it. Our <code>age</code> column in customers has about 4 percent missing. Compare options.</p>
@@py
import pandas as pd
c = pd.read_csv(DATA + "customers.csv")
print("missing ages:", c.age.isna().sum(), "of", len(c))
print("mean", round(c.age.mean(), 2), "| median", c.age.median())
print(c.groupby("segment").age.median().to_dict())
by_seg = c.age.fillna(c.groupby("segment").age.transform("median"))
print("after group-median fill: missing", by_seg.isna().sum(), "| overall mean", round(by_seg.mean(), 2))
@@
<p>Filling by segment respects the fact that Students are younger (median 22) than other segments; a single global fill would put a 34-year-old into the Student group. Better still, keep an <code>age_missing</code> flag so a model can learn if missingness matters.</p>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Filling "not applicable" with zero.</strong> Wrong: setting missing delivery_minutes to 0 for cancelled orders. The average delivery time then drops, because about 2,800 zeros are averaged in. Right: leave it missing; averages and models should skip it, and the late rate uses only orders that have both times.</div></div>
<h3>Missing values in Excel, Power BI and R (not run here)</h3>
@@table
Tool | Detect | Fill
Excel | <code>=COUNTBLANK(Orders[city])</code> | <code>=IF([@unit_price]="", XLOOKUP([@product], Products[product], Products[list_price]), [@unit_price])</code>; Go To Special, Blanks to fill with a constant
Power Query | Column quality bar shows Empty percentage | Merge Queries with Products, then Add Column, Conditional Column; or Transform, Replace Values, null with Unknown; Fill Down for sorted data
DAX | <code>COUNTBLANK(Orders[city])</code> | <code>Price Clean = COALESCE(Orders[unit_price], RELATED(Products[list_price]))</code> (needs a relationship on product)
R | <code>colSums(is.na(orders))</code> | <code>orders %&gt;% left_join(products) %&gt;% mutate(unit_price = coalesce(unit_price, list_price))</code>
@@

<h2>3.5 Outliers: errors versus extremes</h2>
<p>An outlier is a value far from the rest. Two different things hide behind the word: <strong>errors</strong> (a quantity of 99 where the maximum possible basket is a handful; a delivery time of minus 12 minutes) and <strong>genuine extremes</strong> (a legitimate rural delivery that took 3 hours). Errors are fixed or removed; extremes are kept, perhaps capped for a model. Only domain knowledge separates them.</p>
<p>Two common statistical detectors: the <strong>IQR rule</strong> (flag values below Q1 − 1.5 × IQR or above Q3 + 1.5 × IQR, where IQR = Q3 − Q1) and the <strong>z-score</strong> (flag values more than 3 standard deviations from the mean). IQR is robust because quartiles ignore extremes; z-scores are distorted by the very outliers they hunt.</p>
@@py
import pandas as pd
o = pd.read_csv(DATA + "orders.csv").drop_duplicates()
d = o.delivery_minutes.dropna()
q1, q3 = d.quantile([.25, .75])
lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
z = (d - d.mean()) / d.std()
print(f"Q1={q1} Q3={q3} IQR fences: {lo:.1f} to {hi:.1f}")
print("IQR flags :", ((d < lo) | (d > hi)).sum(), "| of which above 300:", (d > 300).sum(), "| negative:", (d < 0).sum())
print("z>3 flags :", (z.abs() > 3).sum())
print("domain rule (outside 5..300):", ((d < 5) | (d > 300)).sum())
print("mean with errors", round(d.mean(), 2), "| median", d.median(), "| mean without errors", round(d[d.between(5, 300)].mean(), 2))
@@
<p>The IQR rule flags more rows than the domain rule because a right-skewed distribution has a long legitimate tail (a 75-minute delivery in rain is slow but real). The z-score rule flags fewer, because the 2,900 outliers inflate the standard deviation. The domain rule (nobody delivers in under 5 minutes or over 5 hours) matches the planted errors and no real ones. We use it, and also keep the slow-but-genuine deliveries because Chapter 6 tries to predict them.</p>
<div class="callout green"><div class="lab">KEY IDEA</div><div class="txt">Use statistics to <em>find</em> suspects, domain rules to <em>decide</em>. And always compare the metric with and without the suspects, as in the last line above: a mean moved by a few absurd rows is a different story from one that barely changes.</div></div>
<div class="callout red"><div class="lab">COMMON MISTAKE</div><div class="txt"><strong>Deleting every outlier.</strong> Wrong: removing the top 1 percent of order values because they "look odd". They are your best customers; revenue shrinks and the model never sees a big basket. Right: investigate, fix errors, keep real extremes, and report both versions of any sensitive metric.</div></div>
<h3>Outliers in Excel, Power BI and R (not run here)</h3>
@@table
Tool | Recipe
Excel | <code>=QUARTILE.INC(range,1)</code> and <code>=QUARTILE.INC(range,3)</code> for fences; conditional formatting with a formula <code>=OR(K2&lt;5, K2&gt;300)</code>; or a box plot chart (Insert, Statistic Chart, Box and Whisker)
Power Query | Add Column, Conditional Column: if delivery_minutes &lt; 5 or &gt; 300 then null; the column profile shows min, max and distribution
DAX | <code>Clean Minutes = IF(OR(Orders[delivery_minutes] &lt; 5, Orders[delivery_minutes] &gt; 300), BLANK(), Orders[delivery_minutes])</code>
R | <code>boxplot.stats(x)$out</code> lists IQR-rule outliers
@@

<h2>3.6 Types, dates and units</h2>
<p>A type error is a silent bug: text that looks like a number sorts as text ("10" before "9"), a date read as text cannot be subtracted, and an id read as a float turns 1001 into 1001.0, which then fails to match a text id. The checklist: ids as integers or strings (never floats), dates as dates, money as decimals with one currency, flags as booleans, categories as a controlled set.</p>
@@py
import pandas as pd
o = pd.read_csv(DATA + "orders.csv")
print(o.dtypes.to_string())
o["order_date"] = pd.to_datetime(o["order_date"])
print("days in range:", (o.order_date.max() - o.order_date.min()).days + 1)
print("text sort:", sorted(["10", "9", "100"]), "| number sort:", sorted([10, 9, 100]))
o["month"] = o.order_date.dt.to_period("M").astype(str)
print(o.month.nunique(), "months; first", o.month.min())
@@
<p>After <code>to_datetime</code> you can take differences, extract the month, weekday or hour, and group by period. Missing numbers force pandas to use floats, which is why <code>promised_minutes</code> and <code>unit_price</code> appear as <code>float64</code>; the newer nullable integer types (<code>Int64</code>) avoid that when you need true integers with gaps.</p>
@@table
Tool | Type fixing
SQL (SQLite) | Dates are text in ISO form; use <code>date()</code>, <code>strftime('%Y-%m', order_date)</code>; cast with <code>CAST(x AS INTEGER)</code>
pandas | <code>pd.to_datetime</code>, <code>astype</code>, <code>pd.to_numeric(errors="coerce")</code> turns bad text into missing
Excel | Text to Columns, <code>=DATEVALUE()</code>, Format Cells; beware locale-dependent parsing
Power Query | The type icon in each header; Change Type with Locale for dates in another convention
R | <code>as.Date()</code>, <code>as.numeric()</code>, readr <code>col_types</code>
@@

<h2>3.7 What cleaning did to the answers</h2>
<p>The point of a log is to show the effect of each rule. We apply the rules one after another and track the headline metrics, in pandas with the exact same order as <code>prep.py</code>.</p>
@@py
import pandas as pd
o = pd.read_csv(DATA + "orders.csv")
p = pd.read_csv(DATA + "products.csv")
price = lambda d: d.unit_price.fillna(d["product"].map(p.set_index("product")["list_price"]))
rev = lambda d: (d.quantity * price(d) * (1 - d.discount))[d.status == "delivered"].sum()
log = [("raw file", len(o), rev(o))]
o = o.drop_duplicates();                 log.append(("drop 150 exact duplicates", len(o), rev(o)))
o = o[o.quantity <= 20];                 log.append(("drop quantity > 20", len(o), rev(o)))
raw_missing_price = o.unit_price.isna().sum()
rows = pd.DataFrame(log, columns=["step", "rows", "delivered_revenue"])
rows["change"] = rows.delivered_revenue.diff().round(0)
print(rows.round(0).to_string(index=False))
nofill = (o.quantity * o.unit_price * (1 - o.discount))[o.status == "delivered"].sum()
print("revenue if missing prices are NOT filled:", round(nofill), "| fill adds", round(rev(o) - nofill))
@@
<p>Duplicates and absurd quantities move revenue by a visible amount, the missing prices by a smaller one, and city spelling does not change total revenue at all but changes <em>every city's total</em>. A cleaning step that leaves the grand total untouched can still change the ranking. That is why Chapter 1's Q4 ("top city") cannot be answered before cleaning.</p>
@@table
Rule | Rows affected | Metric affected
Drop exact duplicates | 150 | orders, revenue, return rate
Drop quantity above 20 | 5 | revenue (outliers dominate)
Standardise city | thousands of labels, no rows dropped | city ranking, not totals
Fill price from catalogue | 90 | revenue
Channel missing to Unknown | about 60 | channel mix
Impossible delivery times to missing | 20 | average delivery, late rate
@@

<h2>3.8 Which tool for which cleaning job</h2>
@@table
Cleaning job | SQL | pandas | Excel | Power Query / Power BI | R
Exact duplicates | DISTINCT, GROUP BY | drop_duplicates | Remove Duplicates | Remove Duplicates | distinct
Standardise text | LOWER, TRIM, CASE | str methods, map | TRIM, PROPER, XLOOKUP | Format, Replace Values, Merge | stringr, recode
Fill from a lookup | LEFT JOIN, COALESCE | map, merge | XLOOKUP | Merge Queries | left_join, coalesce
Flag or cap outliers | CASE WHEN | clip, where | IF, conditional format | Conditional Column | pmin, pmax
Fix types and dates | CAST, strftime | to_datetime | Text to Columns | Change Type | as.Date
Audit trail | Views and scripts | Script in Git | Weak | Applied Steps list | Script in Git
Scale | Millions of rows | Millions in memory | About 1 million rows | Millions (compressed) | Millions in memory
@@
<p>The practical rule: if the cleaning must repeat on every refresh, it belongs in a script, a SQL view or Power Query steps. If it is a one-off exploration of a few hundred rows, Excel is fine. If it needs judgement and statistics (imputation, outlier analysis), use pandas or R.</p>
<h3>Going deeper: the cleaning log as a contract</h3>
<p>Write the cleaning log as data: a small table with columns rule, reason, rows affected, owner, date. When the CEO asks why revenue differs from finance's number, the log answers in a minute. Teams that skip it spend days reconstructing what happened. Add one more habit from Chapter 2: put the checks of the cleaned table (unique ids, only five cities, no delivery time outside 5 to 300) in the pipeline, so a regression in the cleaning breaks the build rather than the dashboard.</p>

<h2>Chapter recap</h2>
<ul><li>Cleaning is five moves: detect, decide, act, verify, log.</li><li>Drop exact duplicates; for partial duplicates define which copy wins.</li><li>Standardise text by trim, lowercase and an explicit alias map; unknown values should turn into missing, not pass through.</li><li>Missing is several things: not applicable, lookup available, random, informative.</li><li>Fill from a lookup if you can, from a group median otherwise, and flag what you filled.</li><li>Find outliers statistically, decide with domain rules, keep real extremes.</li><li>Fix types early: dates as dates, ids as integers, no floats for ids.</li><li>Report the effect of each rule on the headline metrics.</li><li>Cleaning in code or recorded steps is repeatable; hand edits are not.</li></ul>
@@table
Pattern | Meaning
<code>drop_duplicates()</code> / <code>SELECT DISTINCT</code> | Remove exact repeated rows
<code>.str.strip().str.lower().map(alias)</code> | Normalise then map to canonical names
<code>COALESCE(a, b)</code> / <code>fillna</code> | First non-missing value
IQR fences Q1 − 1.5 IQR, Q3 + 1.5 IQR | Statistical outlier suspects
Domain rule (5 to 300 minutes) | Decides which suspects are errors
Cleaning log | Rule, reason, rows, effect
@@

<h2>Practice set</h2>
@@qa 3.9
Q: How many exact duplicate rows does orders.csv contain, and how many rows remain after dropping them?
A: ~~len(raw)-len(raw.drop_duplicates())~~ duplicates; ~~len(raw.drop_duplicates()):,~~ rows remain (before the quantity rule; after it ~~len(o):,~~).
Q: Why is dropping duplicates on customer_id and product alone wrong?
A: Customers legitimately buy the same product more than once; you would delete real orders.
Q: Normalise "Bangalore ", "BENGALURU" and "bangalore" to a single name in one pandas expression.
A: <code>s.str.strip().str.lower().map({"bangalore": "Bengaluru", "bengaluru": "Bengaluru"})</code>; all three become Bengaluru.
Q: After mapping, how many orders have a missing city, and are they spelling problems?
A: ~~o.city.isna().sum()~~ orders (cleaned file). They were missing in the source, not misspelled; they need a separate decision (Unknown label or exclusion).
Q: List the four kinds of missing value and give a ShopKart example of each.
A: Not applicable (delivery time of a pickup), lookup available (price), random (channel), informative (age).
Q: Write SQL that fills a missing unit price from the products table.
A: <code>SELECT COALESCE(o.unit_price, p.list_price) FROM orders o JOIN products p ON p.product = o.product;</code>
Q: Quartiles of a variable are 30 and 45 minutes. Compute the IQR fences.
A: IQR = 15; lower = 30 − 22.5 = 7.5; upper = 45 + 22.5 = 67.5 minutes.
Q: Why does a z-score rule find fewer outliers than the IQR rule when a few extreme values exist?
A: The extremes inflate the standard deviation, so z-scores of everything shrink (masking). Quartiles are robust.
Q: What is the delivery-time domain rule used here and what does it flag?
A: Keep 5 to 300 minutes; it flags 20 values (12 extreme such as 480 to 2,900, and 8 negative), all planted errors.
Q: Find the bug: <code>df.city = df.city.fillna(0)</code>.
A: Zero is a number in a text column; it creates a fake city called 0 and breaks groupings. Use "Unknown" or leave missing.
Q: Explain why cleaning the city column changes the top-city ranking but not total revenue.
A: Cleaning moves revenue between labels (four Bengaluru spellings merge) but each row keeps its revenue, so the sum is unchanged.
Q: Interview style: "Your colleague fixed errors by editing the Excel file. What is the risk and what do you propose?"
A: The edits are untraceable and cannot be reapplied to new data. Replace them with a script or Power Query steps plus a cleaning log, and keep the raw file untouched.
@@

<h2>Prompt pack</h2>
@@prompt
You are my patient, practical professor. I am a working professional moving into data roles. Teach me data cleaning with an online-shop example: duplicates, inconsistent text, missing values, outliers and types. For each, ask me to choose a rule and justify it, then show me the pandas, SQL and Excel way. One question at a time, with feedback.
@@
@@prompt
Act as a data quality reviewer. Here is my cleaning code and the log of what it changed: [paste]. Check whether each rule is justified, whether any rule hides information (for example filling "not applicable" with zero), whether the order of rules matters, and which metric each rule moves. Suggest two additional checks.
@@
@@prompt
Run a mock interview for a data analyst role focused on data cleaning. Give me a messy table description (duplicates, mixed date formats, missing prices, outliers) and ask what I would do, in which tool and why. Push back on vague answers. Finish with a grade.
@@
