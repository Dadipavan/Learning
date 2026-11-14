# ---------- 3.5 glossary and mental model ----------
mk=X("""CREATE TABLE marks (student TEXT, subject TEXT, mark INTEGER);
INSERT INTO marks VALUES
 ('Asha','maths',78),('Asha','science',85),
 ('Ravi','maths',62),('Ravi','science',NULL),
 ('Meena','maths',91),('Meena','science',74),
 ('John','maths',55),('John','science',68);
SELECT * FROM marks;""")
mk2=X("""SELECT subject, COUNT(*) AS n_rows, COUNT(mark) AS n_marks, SUM(mark) AS total,
       MIN(mark) AS lowest, MAX(mark) AS highest
FROM marks
GROUP BY subject;""")
t1=X("""SELECT COUNT(*) AS lines_after_join
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id;""")
t2=X("""SELECT COUNT(*) AS lines_after_where
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid';""")
t3=X("""SELECT COUNT(*) AS n_groups FROM (
  SELECT o.customer_id
  FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
  WHERE o.status = 'paid'
  GROUP BY o.customer_id);""")
t4=X("""SELECT o.customer_id, SUM(oi.qty * oi.unit_price) AS spent
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'paid'
GROUP BY o.customer_id
HAVING SUM(oi.qty * oi.unit_price) > 1500
ORDER BY spent DESC;""")
e1=ERR("""SELECT customer_id, COUNT(*) FROM orders WHERE COUNT(*) > 2 GROUP BY customer_id;""")
body=f'''
<h2 id="x5-3-5-glossary-and-the-mental-model">3.5 Glossary and the Mental Model (read this first if aggregation feels fuzzy)</h2>
{co("blue","INTUITION","Picture a school attendance register with 40 names. The principal does not want 40 names. She wants one number: how many are present today. Taking many rows and answering with one number is <em>aggregation</em>. If she asks 'how many present <em>in each class</em>', you first sort the register into class piles, then count each pile. That second step is <code>GROUP BY</code>. If she then says 'only show classes with fewer than 30 present', you throw away whole piles after counting. That is <code>HAVING</code>. Every query in this chapter is some mix of sort into piles, collapse each pile to a number, and keep or drop piles.")}
<p>The words below are used all through the chapter. Skim them now and come back whenever a term feels slippery.</p>
{tbl(["Word","Plain meaning","Example in our shop"],[
["row","one record in a table; one line of the register","order line (order 101, product 3, qty 2)"],
["aggregate function","a function that reads many rows and returns <em>one</em> value","<code>SUM(qty)</code>, <code>COUNT(*)</code>, <code>MAX(price)</code>"],
["group (pile)","all rows that share the same value of the grouping key","all rows with <code>status = 'paid'</code>"],
["grouping key","the column or expression you sort rows into piles by","<code>customer_id</code>, <code>substr(order_date,1,7)</code>"],
["grain","what one row of the <em>result</em> stands for, written as 'one row per ___'","one row per customer per month"],
["NULL","'value unknown or missing', not zero and not an empty string","an order with no coupon"],
["predicate","a condition that is true, false or unknown","<code>status = 'paid'</code>"],
["conditional aggregate","an aggregate that only reads the rows meeting a condition","<code>COUNT(*) FILTER (WHERE status='refunded')</code>"],
["fan-out","a join that repeats one row several times, inflating counts and sums","an order repeated once per item line"],
["scalar","a single value (one row, one column)","the number 14560"],
["reconcile","check that parts add up to the whole","per-product revenue adds to 14560"]])}
<h3>The mental model in five sentences</h3>
<ol><li>The database first decides <em>which rows</em> exist: <code>FROM</code> and <code>JOIN</code> build the rows, <code>WHERE</code> throws away the ones you do not want.</li><li><code>GROUP BY</code> sorts the surviving rows into piles by the key. With no <code>GROUP BY</code> the whole table is one pile.</li><li>Each aggregate function turns each pile into one value.</li><li><code>HAVING</code> throws away whole piles, using those values.</li><li>Only then does <code>SELECT</code> produce the output columns, followed by <code>ORDER BY</code> and <code>LIMIT</code>.</li></ol>
{fig("ch03d_pipeline.png","Six boxes in a row: FROM and JOIN 20 rows, WHERE 18 rows, GROUP BY 5 groups, HAVING 3 groups, SELECT 3 rows, ORDER BY 3 rows","The logical order in which the database processes a grouped query, with the real row counts for 'paid spend per customer, only above 1500'.","read left to right. The first box builds 20 order lines. <code>WHERE</code> drops the 2 lines that belong to non-paid orders (order 104 has one line, order 109 has one line), leaving 18. <code>GROUP BY</code> sorts those 18 lines into 5 piles, one per paying customer. <code>HAVING</code> keeps the 3 piles whose sum exceeds 1500. <code>SELECT</code> and <code>ORDER BY</code> only format what is left. The red sentence under the boxes is the key rule of the chapter: a clause can only use things that already exist when it runs.")}
{P("3.5.1","Trace the query 'paid spend per customer, only customers above 1500' step by step and write down how many rows or groups remain after each stage. Predict first: the shop has 20 order lines, order 104 (cancelled) has 1 line and order 109 (refunded) has 1 line.")}
{t1}
{t2}
{t3}
{t4}
{steps([("Stage 1","<code>FROM ... JOIN</code> gives one row per order line: 20."),("Stage 2","<code>WHERE status = 'paid'</code> removes the lines of order 104 (cancelled) and order 109 (refunded): 20 - 1 - 1 = 18."),("Stage 3","<code>GROUP BY customer_id</code> sorts the 18 lines into piles. Customers 1, 2, 4, 5 and 6 have paid lines (customer 3 had only the cancelled order, so there is no pile): 5 groups."),("Stage 4","<code>HAVING SUM(...) &gt; 1500</code> keeps customers 1 (4560), 2 (3600) and 4 (3300). Customer 5 has 760 and customer 6 has 440: 3 groups."),("Answer","The final output has 3 rows, one per surviving customer, sorted by spent."),("Check","The counts go 20, 18, 5, 3 and each step can only shrink or keep the count. If a count ever grows after a stage, something multiplied rows.")])}
{P("3.5.2","Do <code>GROUP BY</code> by hand on a tiny table before trusting the database. The table <code>marks</code> has 8 rows (4 students times 2 subjects). One mark, Ravi's science mark, is NULL because he was absent. Find the number of rows, the number of real marks, the total, the lowest and the highest mark per subject.")}
{mk}
{mk2}
{steps([("Step 1","Make two piles by the key <code>subject</code>. Maths pile: 78, 62, 91, 55. Science pile: 85, NULL, 74, 68."),("Step 2 (maths)","4 rows and 4 real marks. Sum: 78 + 62 + 91 + 55 = 286. Lowest 55, highest 91."),("Step 3 (science)","4 rows but only 3 real marks (85, 74, 68). The NULL is skipped by <code>COUNT(mark)</code>, <code>SUM</code>, <code>MIN</code> and <code>MAX</code>. Sum: 85 + 74 + 68 = 227. Lowest 68, highest 85."),("Check","The printed table matches both hand piles. <code>COUNT(*)</code> counted the absent student, <code>COUNT(mark)</code> did not."),("Meaning","Two different questions hide here: 'how many students were enrolled' (4) and 'how many marks were recorded' (3). Pick the function that matches the question.")])}
{P("3.5.3","A teammate writes <code>WHERE COUNT(*) &gt; 2</code> to find customers with more than two orders. What does the database say, and why?")}
{e1}
{steps([("Step 1","Follow the pipeline. <code>WHERE</code> is stage 2, applied to one row at a time."),("Step 2","At that moment no pile exists, so there is no <code>COUNT(*)</code> for a customer yet."),("Step 3","The database refuses: an aggregate is not allowed where only single rows are visible."),("Fix","Move the test to <code>HAVING COUNT(*) &gt; 2</code>, which runs at stage 4, after the piles exist."),("Answer","The error is a pipeline-order error, not a typing error. When you see 'misuse of aggregate', ask: which stage am I in?")])}
{co("red","COMMON MISTAKE","Putting an aggregate in <code>WHERE</code>. Wrong: <code>WHERE COUNT(*) &gt; 2</code> (error: misuse of aggregate). Right: <code>GROUP BY customer_id HAVING COUNT(*) &gt; 2</code>. The reverse mistake also exists: using <code>HAVING status = 'paid'</code> for a plain row condition. It works, but it makes the database build piles for every status first and then discard them. Put row conditions in <code>WHERE</code>.")}
<p><strong>Check yourself.</strong> (1) In which stage is a column alias from <code>SELECT</code> created? Answer: stage 5, after <code>HAVING</code>, which is why strict databases refuse the alias earlier. (2) With no <code>GROUP BY</code>, how many piles are there? Answer: one, the whole table. (3) What is the grain of Problem 3.5.2's result? Answer: one row per subject.</p>
'''
ins("d1",body)
