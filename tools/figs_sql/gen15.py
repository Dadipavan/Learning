from _kit import *
db=sqlite3.connect("/tmp/proj/p15.db")
X=lambda c: exec_sql(db,c)
conv=X("""SELECT u.channel,
       count(DISTINCT u.user_id) AS users,
       count(DISTINCT o.user_id) AS buyers,
       round(100.0 * count(DISTINCT o.user_id) / count(DISTINCT u.user_id), 1) AS conv_pct
FROM users u LEFT JOIN orders o ON o.user_id = u.user_id
GROUP BY u.channel ORDER BY conv_pct;""")
tot=X("SELECT round(sum(amount), 2) AS revenue, count(*) AS orders FROM orders;")
good=X("""SELECT u.channel, round(sum(o.amount), 1) AS revenue
FROM orders o JOIN users u ON u.user_id = o.user_id
GROUP BY u.channel ORDER BY u.channel;""")
bad=X("""SELECT u.channel, round(sum(o.amount), 1) AS revenue
FROM orders o
JOIN users u  ON u.user_id = o.user_id
JOIN events e ON e.user_id = u.user_id          -- several events per user: duplicates each order
GROUP BY u.channel ORDER BY u.channel;""")
cnt=X("""SELECT count(*) AS joined_rows, (SELECT count(*) FROM orders) AS orders FROM orders o JOIN events e ON e.user_id = o.user_id;""")
fix=X("""SELECT u.channel, round(sum(o.amount), 1) AS revenue, count(*) AS orders
FROM orders o JOIN users u ON u.user_id = o.user_id
GROUP BY u.channel
UNION ALL
SELECT 'TOTAL', round(sum(amount), 1), count(*) FROM orders;""")
z='''import math
# social: 96 buyers of 906 users.  search: 272 buyers of 1201 users.
x1, n1, x2, n2 = 96, 906, 272, 1201
p1, p2 = x1 / n1, x2 / n2
pool = (x1 + x2) / (n1 + n2)
se = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
z = (p2 - p1) / se
print("social %.1f%%  search %.1f%%  gap %.1f points" % (100 * p1, 100 * p2, 100 * (p2 - p1)))
print("z = %.1f" % z)
se_gap = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
lo, hi = (p2 - p1) - 1.96 * se_gap, (p2 - p1) + 1.96 * se_gap
print("95%% interval for the gap: %.1f to %.1f points" % (100 * lo, 100 * hi))
'''
zo=pyrun(z)
body=f'''
<h2 id="x15-5-worked-extension-segment-the-funnel-catch-a-fan-out-and-test-the-gap">15.5 Worked Extension: Compare Channels, Catch a Fan-Out and Test the Gap</h2>
{co("blue","INTUITION","A project is not finished when the queries run. It is finished when someone can trust the numbers and act on them. This walkthrough takes the funnel database from Section 15.2 (3,000 users, 6,345 events, 1,209 orders, built by its generator with seed 42) and does the three things a reviewer will ask: compare segments, check that totals reconcile, and say whether a gap is real. The SQL output below was produced by running the generator and these queries on SQLite 3.50.4.")}
<h3>Step 1: conversion by channel</h3>
{P("15.5.1","What share of each channel's users ever bought? Predict first: the planted pattern says social is worst, referral and email best.")}
{conv}
{steps([("Step 1","A <code>LEFT JOIN</code> keeps users who never bought, so the denominator is all users in the channel. <code>count(DISTINCT o.user_id)</code> counts each buyer once however many orders they placed."),("Step 2","Social converts 10.6 percent (96 of 906). Search is 22.6, email 30.9, referral 32.4."),("Check","Buyers add up: 96 + 272 + 187 + 93 = 648, which equals the 648 users who reached the <code>pay</code> step in the funnel. Two independent routes agree."),("Meaning","Social brings the most users after search but the fewest buyers per user. That is the first finding for the report.")])}
<h3>Step 2: reconcile revenue, and see a fan-out happen</h3>
<p>Now revenue by channel. First the total it must add up to:</p>
{tot}
{P("15.5.2","Compute revenue per channel correctly, then show what a careless extra join does to it. Predict first: the correct pieces add to 65,574.04, and the careless version inflates them several times over, because each user has several events.")}
{good}
<p>Those four numbers add to 65,574.0, the total. Now someone adds a join to <code>events</code> 'to also show the number of events':</p>
{bad}
{cnt}
{steps([("Step 1","Each order row is matched with every event row of the same user. A user with 4 events makes each of their orders appear 4 times."),("Step 2","The row count tells the story: 4,836 joined rows against 1,209 orders, a factor of 4.0 on average, so every revenue figure is about 4 times too large (email 83,194.1 against the true 20,798.5)."),("Step 3","No error is raised. The shares by channel look plausible, which is why this bug survives code review.")])}
{co("red","COMMON MISTAKE","Joining two tables that both have many rows per key (orders and events per user) and then summing. The rule: <strong>aggregate each side to one row per key first, then join</strong>, or do not join at all if you do not need the column. Detect it every time with the reconciliation habit: compare <code>count(*)</code> after the join with the count before, and compare the grand total with a query that has no joins.")}
{fix}
<p>The final <code>TOTAL</code> row is the reconciliation built into the output. A reviewer who sees a total that equals the independent figure of 65,574.0 trusts the table.</p>
<h3>Step 3: is the social gap real or noise?</h3>
<p>Social converts 10.6 percent and search 22.6. With 906 and 1,201 users, could that gap be luck? The standard check is a two-proportion z-test (the Statistics document, Chapter 6, explains it fully). The code below computes it by hand:</p>
{P("15.5.3","Test social against search and give an interval for the gap. Predict first: a gap of 12 points on groups of about a thousand is far outside random wobble.")}
{py(z)}
{text(zo)}
{steps([("Step 1","Pool the two groups: (96 + 272) / (906 + 1201) = 17.5 percent buyers overall. Under 'no difference' both channels share that rate."),("Step 2","The standard error of the gap under that assumption combines both group sizes. The z score is the gap divided by it."),("Step 3","A z of about 7.2 is enormous (anything beyond 2 or 3 is already unlikely by chance). The 95 percent interval for the gap runs from about 9.0 to 15.2 points and excludes zero."),("Answer","The gap is real. Write it as: 'social converts 10.6 percent (96 of 906) versus 22.6 percent for search (272 of 1,201); the gap of 12.1 points has a 95 percent interval of 9.0 to 15.2 points.'")])}
{co("green","GOING DEEPER","Significance says the gap is not luck. It does not say why. Social users may be browsing from phones, or arriving from a different campaign, or just less intent. The data cannot separate those; only a test or a better variable can. Say so in the report, in the limits paragraph. Also note the multiple-comparison issue: if you test every pair of channels and every segment, some gaps will pass by chance. Decide the comparisons before you look.")}
<h3>A grading rubric for your own project</h3>
<p>Score yourself 0 to 2 on each line. A score of 12 or more out of 16 is portfolio quality.</p>
{tbl(["Line","0 points","2 points"],[
["Question","missing or vague","one sentence with a measurable answer"],
["Data","unexplained source","seeded generator or documented source, row counts shown"],
["Correctness","totals never checked","every table reconciles to an independent total"],
["Readability","one 80-line query","CTEs with clear names, one idea each"],
["Segment sizes","rates without counts","every rate shows its n"],
["Uncertainty","no comment on noise","at least one gap tested or labelled too small to trust"],
["Writing","list of tables","three findings with numbers, a recommendation, limits"],
["Reproducibility","cannot rerun","README with run order; fresh clone gives the same numbers"]])}
<h3>Practice with answers</h3>
{qa("15.5.4","Referral has 287 users and 93 buyers. Compute its conversion and say how many users you would need in each of social and referral to compare them with confidence. <em>(easy)</em>","93 / 287 = 32.4 percent. The group sizes here (906 and 287) are already large enough, because the gap is more than 20 points. Small gaps need more users, big gaps need fewer.")}
{qa("15.5.5","A revenue table by channel adds to 262,296.2 but finance says 65,574.04. First check? <em>(find the bug)</em>","Compare row counts: <code>count(*)</code> of the final joined result with <code>count(*)</code> of <code>orders</code>. A ratio of 4 points to a join with <code>events</code>. Remove the join or aggregate events to one row per user first.")}
{qa("15.5.6","Why is 'average revenue per user' by channel computed with a <code>LEFT JOIN</code> from users, and what changes with an inner join? <em>(medium)</em>","A <code>LEFT JOIN</code> from <code>users</code> keeps non-buyers, so the denominator is every user, and the average is revenue per <em>visitor</em>. An inner join drops non-buyers, so the denominator is buyers only and the figure is revenue per <em>buyer</em>, much higher, and not comparable across channels with different conversion.")}
'''
insert("15","lab15",body)
