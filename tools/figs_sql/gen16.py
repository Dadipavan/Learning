from _kit import *
db=sqlite3.connect("/tmp/proj/p16.db")
X=lambda c: exec_sql(db,c)
lead=X("""SELECT cast(julianday(appt_date) - julianday(booked_on) AS INTEGER) AS lead_days,
       count(*) AS n,
       sum(status = 'no_show') AS no_shows,
       round(100.0 * sum(status = 'no_show') / count(*), 1) AS no_show_pct
FROM appointments
WHERE status <> 'cancelled'
GROUP BY lead_days ORDER BY lead_days;""")
score=X("""WITH t AS (
  SELECT a.status, d.department,
         cast(julianday(a.appt_date) - julianday(a.booked_on) AS INTEGER) AS lead
  FROM appointments a JOIN doctors d ON d.doctor_id = a.doctor_id
  WHERE a.status <> 'cancelled'
),
s AS (
  SELECT *, (CASE WHEN lead >= 14 THEN 2 WHEN lead >= 5 THEN 1 ELSE 0 END)
            + (department = 'Pediatrics') AS risk_score
  FROM t
)
SELECT risk_score, count(*) AS n, sum(status = 'no_show') AS no_shows,
       round(100.0 * sum(status = 'no_show') / count(*), 1) AS no_show_pct
FROM s GROUP BY risk_score ORDER BY risk_score DESC;""")
pw='''import math
# baseline no-show rate for bookings made 14+ days ahead: 33.8 percent (550 of 1628)
p1 = 550 / 1628
p2 = p1 - 0.05            # we hope reminders cut it by 5 points
z_alpha, z_beta = 1.96, 0.8416      # 95 percent confidence, 80 percent power
d = p1 - p2
n_arm = (z_alpha + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / d ** 2
print("baseline %.1f%%, target %.1f%%" % (100 * p1, 100 * p2))
print("needed per arm: %d, total: %d" % (math.ceil(n_arm), 2 * math.ceil(n_arm)))
per_week = 1628 / 52
print("such bookings per week: %.0f, weeks to fill: %.0f" % (per_week, 2 * math.ceil(n_arm) / per_week))
'''
pwo=pyrun(pw)
body=f'''
<h2 id="x16-3-worked-extensions-the-lead-time-profile-a-risk-score-and-how-big-must-a-test-be">16.3 Worked Extensions: The Lead-Time Profile, a Risk Score and How Big a Test Must Be</h2>
{co("blue","INTUITION","The case study found that booking far ahead causes no-shows. A manager's next questions are always the same: 'how steep is it, exactly?', 'can you give me a list of who to phone?' and 'how long until we know if phoning works?'. This section answers all three on the same clinic data (generator in 16.1, seed 5). Numbers below come from running it on SQLite 3.50.4.")}
<h3>Extension 1: the full lead-time profile</h3>
<p>Section 16.1 used lead-time bands. Bands hide the shape, so first look at every distinct lead value. Cancelled appointments are excluded because they never had a chance to be a no-show.</p>
{P("16.3.1","Compute the no-show rate for each lead time, with the group size. Predict first: the rate rises with lead time, from under 10 percent for same-week bookings to around 40 percent for 30 days.")}
{lead}
{fig("ch16_lead.png","Bar chart of no-show rate by lead time, rising from 8 percent at 0 days to 41 percent at 30 days, with group sizes inside the bars","No-show rate by lead time on the 5,485 non-cancelled appointments.","each bar is one lead time, the label on top is the no-show rate and the small white text inside is the group size. All groups have 527 to 588 appointments, so none of the bars is a small-sample accident. The rate is nearly flat for 0 to 2 days (8 to 9 percent), then climbs, and the steepest jump is between 14 and 21 days (24.5 to 35.6 percent).")}
{steps([("Step 1","<code>julianday</code> turns each date text into a day number, so the difference is the lead in days. <code>CAST ... AS INTEGER</code> drops the fraction."),("Step 2","<code>sum(status = 'no_show')</code> adds the true (1) values: SQLite and MySQL treat a comparison as 0 or 1."),("Check","Group sizes add up: 527 + 536 + 543 + 550 + 588 + 545 + 568 + 548 + 540 + 540 = 5,485 = 4,428 attended + 1,057 no-shows. No-shows add up to 1,057."),("Meaning","The relationship is steady and monotone across ten groups of about 550 each. That is much stronger evidence than one gap between two bands.")])}
{co("red","COMMON MISTAKE","Leaving cancelled appointments in the denominator. A cancelled slot was never a no-show and never an attendance, so including it lowers every rate. The case study defines no-show rate among non-cancelled appointments; whichever definition you choose, state it in one line of the report, and use the same one everywhere.")}
<h3>Extension 2: a rule-based risk score and how well it ranks</h3>
<p>Operations cannot phone 5,000 patients. They want a short list. A simple score: 2 points for lead of 14 days or more, 1 point for 5 to 13 days, plus 1 point for Pediatrics (the department with a higher planted rate). Then check how the score separates the groups.</p>
{P("16.3.2","Build the score and report no-show rate per score. Predict first: the rate should rise with the score, and the top two groups should hold most no-shows in a minority of appointments.")}
{score}
{steps([("Step 1","Score 3 (long lead and Pediatrics) has 41.3 percent no-shows (161 of 390). Score 0 has 9.0 percent (148 of 1,643). The score ranks well."),("Step 2","Coverage: scores 2 and 3 together contain 390 + 1,679 = 2,069 appointments, 37.7 percent of 5,485. They hold 161 + 485 = 646 of the 1,057 no-shows, 61.1 percent."),("Step 3","So phoning only the top 37.7 percent of bookings reaches 61.1 percent of all no-shows. That is a lift of 61.1 / 37.7 = 1.6 over calling people at random."),("Answer","A transparent three-line rule already concentrates the problem. A model might do a little better, but this one can be explained to a receptionist.")])}
{co("red","COMMON MISTAKE","Judging the score on the same data used to invent its thresholds (14 and 5 days came from looking at the profile above). The lift is optimistic. Fix: invent the rule on the first half of the year and measure it on the second half (<code>WHERE appt_date &gt;= '2024-07-01'</code>), as you would for any model. Expect a slightly smaller lift.")}
<h3>Extension 3: how big must a reminder test be?</h3>
<p>The clinic has no reminder data, so it must run a test. Before running one, answer: how many bookings, and how many weeks? Let us plan for the group at highest risk, bookings made 14 or more days ahead, where 550 of 1,628 appointments were no-shows (33.8 percent). We hope reminders cut that by 5 points, and we want 95 percent confidence with 80 percent power (an 80 percent chance to detect a real 5-point drop).</p>
{P("16.3.3","Compute the sample size per arm and the time needed. Predict first: a 5-point change on a 34 percent base needs roughly 1,300 per arm, about 2,600 bookings in all, which is more than a year of such bookings.")}
{py(pw)}
{text(pwo)}
{steps([("Formula","n per arm = (z<sub>alpha</sub> + z<sub>beta</sub>)<sup>2</sup> x (p1(1 - p1) + p2(1 - p2)) / (p1 - p2)<sup>2</sup>, with z<sub>alpha</sub> = 1.96 and z<sub>beta</sub> = 0.8416."),("Plug in","p1 = 0.338, p2 = 0.288. Variance part: 0.338 x 0.662 + 0.288 x 0.712 = 0.2238 + 0.2051 = 0.4289. Numerator: 2.8016<sup>2</sup> x 0.4289 = 7.849 x 0.4289 = 3.366. Divide by 0.05<sup>2</sup> = 0.0025: about 1,346 per arm."),("Time","The code gives the exact count and shows that at 31 qualifying bookings a week, 2,692 bookings take about 86 weeks, more than a year and a half."),("Meaning","Run the test across all departments, or accept a larger effect to detect (a 10-point drop needs about a quarter of the sample), or extend the test over more than one clinic. Deciding this before the test is how you avoid a result nobody can trust.")])}
{co("green","GOING DEEPER","Sample size grows with the square of 1 over the effect. Halve the effect you want to detect and you need four times the people. That is why small improvements are expensive to prove and why analysts who promise 'we will see in two weeks' without this calculation are guessing. The same arithmetic sits behind A/B test planning in the Statistics document (Chapter 6).")}
<h3>Practice with answers</h3>
{qa("16.3.4","Group sizes are 527 and 540 and the rates are 8.0 and 41.5 percent. Is it worth testing whether that gap is real? <em>(easy)</em>","No. A 33.5-point gap on groups of about 530 is far beyond random wobble (a difference of 3 or 4 points would be borderline at that size). Spend the time on what to do about it.")}
{qa("16.3.5","The risk score gives scores 0 to 3. Why not phone only score 3? <em>(medium)</em>","Score 3 holds 390 appointments and 161 no-shows, only 15.2 percent of all no-shows. Reaching 61 percent needs scores 2 and 3, which is 2,069 calls. The choice is a trade-off between calls (cost) and no-shows reached (benefit); put both numbers in front of the manager.")}
{qa("16.3.6","Write the query that measures the rule only on appointments after 1 July. <em>(medium)</em>","Add <code>AND a.appt_date &gt;= '2024-07-01'</code> to the <code>WHERE</code> of the CTE <code>t</code>, and keep the thresholds fixed from the first half. Report the new lift next to the old one.")}
{qa("16.3.7","The test runs, and reminders arm shows 29 percent against 34 percent in control, with 600 per arm. A manager says 'it works'. Your answer? <em>(interview)</em>","With 600 per arm the standard error of the gap is about 2.7 points, so a 5-point gap is only about 1.9 standard errors and an interval would run from roughly 0 to 10 points. It is promising, not proven. The planned test needed about 1,350 per arm; either keep running or report the interval honestly.")}
'''
insert("16","lab16",body)
