from _kit import *
db=shop()
X=lambda c: exec_sql(db,c)
nf=X("""SELECT order_id, coupon FROM orders WHERE order_id IN (101, 102) ORDER BY order_id;
SELECT count(*) AS plain_not_equal FROM orders WHERE coupon <> 'SAVE10';
SELECT count(*) AS null_safe_not_equal FROM orders WHERE coupon IS NOT 'SAVE10';
SELECT count(*) AS with_or_null FROM orders WHERE coupon <> 'SAVE10' OR coupon IS NULL;""")
nl=X("""SELECT referrer_id, name FROM customers ORDER BY referrer_id, name LIMIT 4;
SELECT referrer_id, name FROM customers ORDER BY referrer_id DESC, name LIMIT 4;
SELECT referrer_id, name FROM customers ORDER BY referrer_id NULLS LAST, name LIMIT 4;
SELECT referrer_id, name FROM customers ORDER BY referrer_id DESC NULLS LAST, name LIMIT 4;""")
cl=X("""CREATE TABLE tag (word TEXT);
INSERT INTO tag VALUES ('Apple'), ('apple'), ('Banana'), ('banana'), ('cherry');
SELECT word FROM tag ORDER BY word;
SELECT word FROM tag ORDER BY word COLLATE NOCASE, word;
SELECT count(*) AS exact_match FROM tag WHERE word = 'apple';
SELECT count(*) AS nocase_match FROM tag WHERE word = 'apple' COLLATE NOCASE;""")
ty=X("""CREATE TABLE ph (id INTEGER, phone TEXT, age INTEGER);
INSERT INTO ph VALUES (1, '0551', 30), (2, '551', 31), (3, '5.5', 32);
SELECT id, typeof(phone) AS t_phone, typeof(age) AS t_age FROM ph;
SELECT id FROM ph WHERE phone = 551;
SELECT id FROM ph WHERE phone = '551';
SELECT 10 / 4 AS int_div, 10 / 4.0 AS real_div;""")
body=f'''
<h2 id="x2-5-null-safe-comparison-ordering-nulls-collation-and-type-traps">2.5 NULL-Safe Comparison, Ordering NULLs, Collation and Type Traps</h2>
{co("blue","INTUITION","Section 2.4 taught that NULL means 'unknown', so comparing anything with NULL gives unknown, not true or false. Four everyday situations follow from that and surprise beginners: inequality silently drops NULL rows, NULLs sort to an end you did not choose, text sorts differently from what a person expects, and numbers stored as text compare in odd ways. This section shows each one on real rows.")}
<h3>Example 1: not-equal that loses rows, and the NULL-safe fix</h3>
{P("2.5.1","Count orders whose coupon is not 'SAVE10'. Of 14 orders, 3 use SAVE10 and 11 do not. Predict first: a careless <code>&lt;&gt;</code> returns far fewer than 11, because the NULL coupons vanish. Every non-NULL coupon here is SAVE10, so it may return 0.")}
{nf}
{steps([("Step 1","The 3 orders with a coupon all have SAVE10, so <code>coupon &lt;&gt; 'SAVE10'</code> is false for them. For the 11 orders with a NULL coupon it is unknown, which <code>WHERE</code> treats as not true. So the first count is 0, not 11."),("Step 2","<code>IS NOT</code> is SQLite's null-safe not-equal: it treats NULL as an ordinary value. The count is 11. PostgreSQL, SQL Server 2022 and MySQL spell it <code>IS DISTINCT FROM</code> (MySQL: <code>NOT (a &lt;=&gt; b)</code>); not run here."),("Step 3","The portable fix <code>coupon &lt;&gt; 'SAVE10' OR coupon IS NULL</code> also gives 11."),("Meaning","The first query was wrong in a way that gives no error. Always ask: can this column be NULL?")])}
{co("red","COMMON MISTAKE","Using <code>NOT IN</code> with a subquery that can return NULL: <code>WHERE id NOT IN (SELECT referrer_id FROM customers)</code>. If even one <code>referrer_id</code> is NULL, the whole <code>NOT IN</code> is unknown for every row and the query returns nothing. Use <code>NOT EXISTS</code>, or add <code>WHERE referrer_id IS NOT NULL</code> inside the subquery.")}
<h3>Example 2: where do NULLs sort?</h3>
{P("2.5.2","Sort customers by referrer. Predict first: customers 1, 5 and 7 have no referrer. SQLite treats NULL as the smallest value, so ascending puts them first; PostgreSQL treats NULL as the largest, so ascending puts them last.")}
{nl}
{steps([("Step 1","Ascending in SQLite: the NULL referrers (Asha, Priya, Sana) come first. In PostgreSQL and Oracle the default is the opposite, NULLs last on ascending and first on descending."),("Step 2","Descending reverses it: the largest referrer 5 (Kabir) comes first, and NULL rows are last in SQLite."),("Step 3","<code>NULLS FIRST</code> and <code>NULLS LAST</code> (SQLite 3.30+, PostgreSQL, Oracle) make the choice explicit, so the query returns the same order on any database. SQL Server and MySQL do not have the clause; use <code>ORDER BY (col IS NULL), col</code> there."),("Answer","Always state NULL placement when the order matters: a report's 'top 10' will otherwise differ between databases.")])}
<h3>Example 3: case and collation</h3>
<p>A <strong>collation</strong> is the rule that says how text compares and sorts. SQLite's default is binary: capital letters sort before lowercase, and <code>'Apple' = 'apple'</code> is false. PostgreSQL uses the operating-system locale (usually case-aware, ignoring case in the first pass). MySQL's default collations are case-insensitive. Moving a query between systems can therefore change both results and row counts.</p>
{P("2.5.3","Sort and match five words with and without case-insensitivity. Predict first: binary order puts Apple and Banana before apple, banana and cherry.")}
{cl}
{steps([("Step 1","Binary order: all capitals first (Apple, Banana), then lowercase (apple, banana, cherry), because 'A' is code 65 and 'a' is 97."),("Step 2","<code>COLLATE NOCASE</code> sorts Apple next to apple (the extra <code>word</code> sort key then breaks ties in a fixed order)."),("Step 3","Exact match for 'apple' finds 1 row; with NOCASE it finds 2. In PostgreSQL write <code>lower(word) = 'apple'</code> or use <code>ILIKE</code>, or a <code>citext</code> column (not run here).")])}
<h3>Example 4: type traps in SQLite</h3>
<p>SQLite lets a column hold any type unless the table is <code>STRICT</code> (Chapter 9). Its comparison rules convert values in ways PostgreSQL would reject, which hides bugs.</p>
{P("2.5.4","A phone column holds the text '0551', '551' and '5.5'. Look for phone number 551 as a number and as text. Predict first: the numeric literal 551 matches the text '551' only, because the column has TEXT affinity, so 551 is converted to the text '551'.")}
{ty}
{steps([("Step 1","<code>typeof</code> shows what is really stored: text for phone, integer for age."),("Step 2","<code>phone = 551</code> converts the number to text and matches only id 2 ('551'). '0551' is not equal to '551' as text, and a phone number with a leading zero is exactly why phone numbers must be text."),("Step 3","The last row shows that <code>10 / 4</code> is 2 (integer division) and <code>10 / 4.0</code> is 2.5. PostgreSQL does the same for integers; MySQL's <code>/</code> always returns a decimal (use <code>DIV</code> for integers). That difference silently changes percentages written as <code>count / total</code>."),("Answer","Know the stored type, and multiply by <code>1.0</code> (or cast) before dividing.")])}
{co("red","COMMON MISTAKE","Computing a percentage as <code>sum(flag) / count(*) * 100</code>. With integers the division gives 0 whenever the ratio is below 1, so every percentage is 0 or 100. Write <code>100.0 * sum(flag) / count(*)</code>, with the decimal first, as the rest of this book does.")}
<h3>Practice with answers</h3>
{qa("2.5.5","<code>SELECT count(*) FROM customers WHERE referrer_id &lt;&gt; 1</code>. Customers have referrer_ids NULL, 1, 1, 2, NULL, 5, NULL, 3. What is returned? <em>(what is the output?)</em>","The count is 3: the ids 2, 5 and 3 are not equal to 1. The three NULLs are unknown and the two 1s are false, so the answer is 3, not 6.")}
{qa("2.5.6","Make the previous query also count customers without a referrer. <em>(easy)</em>","<code>WHERE referrer_id &lt;&gt; 1 OR referrer_id IS NULL</code>, or <code>IS NOT 1</code> in SQLite, or <code>IS DISTINCT FROM 1</code> in PostgreSQL. The answer is 6.")}
{qa("2.5.7","A teammate ports a query from MySQL to PostgreSQL and the number of rows matching <code>WHERE city = 'pune'</code> falls from 3 to 0. Why? <em>(interview)</em>","MySQL's default collation compares case-insensitively, so 'Pune' matched 'pune'. PostgreSQL compares exactly, so it does not. Fix with <code>lower(city) = 'pune'</code> (and index <code>lower(city)</code>), or <code>ILIKE</code>, or store a normalised column.")}
'''
insert("02","lab2",body)
