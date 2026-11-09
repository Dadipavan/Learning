from _kit import *
fd='''from itertools import combinations
attrs = {"student", "course", "grade", "teacher", "office"}
fds = [({"student", "course"}, {"grade"}), ({"course"}, {"teacher"}), ({"teacher"}, {"office"})]

def closure(x):
    """everything that x determines, by repeatedly applying the rules"""
    x = set(x)
    changed = True
    while changed:
        changed = False
        for left, right in fds:
            if left <= x and not right <= x:
                x |= right
                changed = True
    return x

print("closure of {course}          :", sorted(closure({"course"})))
print("closure of {student,course}  :", sorted(closure({"student", "course"})))
keys = [set(c) for n in range(1, 4) for c in combinations(sorted(attrs), n) if closure(c) == attrs]
minimal = [k for k in keys if not any(o < k for o in keys)]
print("candidate keys:", [sorted(k) for k in minimal])
for left, right in fds:
    ok = closure(left) == attrs
    print("%-18s -> %-8s left side is a superkey: %s" % (",".join(sorted(left)), ",".join(sorted(right)), ok))
'''
fdo=pyrun(fd)
dec='''import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE enrol (student TEXT, course TEXT, grade TEXT, teacher TEXT, office TEXT);
INSERT INTO enrol VALUES
 ('Asha','SQL','A','Rao','B12'), ('Ravi','SQL','B','Rao','B12'),
 ('Asha','Stats','B','Iyer','C03'), ('Meena','Stats','A','Iyer','C03'),
 ('Ravi','ML','A','Iyer','C03');
-- BCNF decomposition from the closure analysis
CREATE TABLE teacher_office (teacher TEXT PRIMARY KEY, office TEXT);
CREATE TABLE course_teacher (course TEXT PRIMARY KEY, teacher TEXT REFERENCES teacher_office);
CREATE TABLE grade_of (student TEXT, course TEXT REFERENCES course_teacher, grade TEXT, PRIMARY KEY (student, course));
INSERT INTO teacher_office SELECT DISTINCT teacher, office FROM enrol;
INSERT INTO course_teacher SELECT DISTINCT course, teacher FROM enrol;
INSERT INTO grade_of SELECT student, course, grade FROM enrol;
""")
rebuilt = db.execute("""SELECT g.student, g.course, g.grade, c.teacher, t.office
  FROM grade_of g JOIN course_teacher c ON c.course = g.course JOIN teacher_office t ON t.teacher = c.teacher
  ORDER BY 1, 2""").fetchall()
original = db.execute("SELECT * FROM enrol ORDER BY 1, 2").fetchall()
print("rows original:", len(original), "| rows rebuilt:", len(rebuilt), "| identical:", rebuilt == original)
db.execute("UPDATE teacher_office SET office = 'D07' WHERE teacher = 'Iyer'")   # one place to change
print(db.execute("SELECT DISTINCT course, office FROM course_teacher c JOIN teacher_office t USING (teacher) ORDER BY 1").fetchall())
'''
deco=pyrun(dec)
sd=pyblock('''import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, deleted_at TEXT);
CREATE UNIQUE INDEX users_email_live ON users(email) WHERE deleted_at IS NULL;
INSERT INTO users (email) VALUES ('a@x.com');
UPDATE users SET deleted_at = '2024-05-01' WHERE email = 'a@x.com';
INSERT INTO users (email) VALUES ('a@x.com');     -- allowed: the old row is soft-deleted
""")
print(db.execute("SELECT id, email, deleted_at FROM users ORDER BY id").fetchall())
try:
    db.execute("INSERT INTO users (email) VALUES ('a@x.com')")   # a second live row with the same email
except sqlite3.IntegrityError as e:
    print("blocked:", e)
print("live users:", db.execute("SELECT count(*) FROM users WHERE deleted_at IS NULL").fetchone()[0])''')
mt=pyblock('''import sqlite3
db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.executescript("""
CREATE TABLE customer (tenant_id INTEGER, customer_id INTEGER, name TEXT, PRIMARY KEY (tenant_id, customer_id));
CREATE TABLE orders (
  tenant_id INTEGER, order_id INTEGER, customer_id INTEGER,
  PRIMARY KEY (tenant_id, order_id),
  FOREIGN KEY (tenant_id, customer_id) REFERENCES customer (tenant_id, customer_id));
INSERT INTO customer VALUES (1, 10, 'Asha'), (2, 10, 'Zed');
INSERT INTO orders VALUES (1, 100, 10);     -- tenant 1 order for tenant 1 customer: fine
""")
try:
    db.execute("INSERT INTO orders VALUES (1, 101, 99)")      # tenant 1 pointing at a customer tenant 1 does not have
except sqlite3.IntegrityError as e:
    print("blocked:", e)
print(db.execute("SELECT * FROM orders").fetchall())''')
po=pyblock('''import sqlite3
db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.executescript("""
CREATE TABLE post (post_id INTEGER PRIMARY KEY);
CREATE TABLE photo (photo_id INTEGER PRIMARY KEY);
CREATE TABLE comment (
  comment_id INTEGER PRIMARY KEY,
  post_id  INTEGER REFERENCES post,
  photo_id INTEGER REFERENCES photo,
  body TEXT,
  CHECK ((post_id IS NOT NULL) + (photo_id IS NOT NULL) = 1)   -- exactly one parent
);
INSERT INTO post VALUES (1); INSERT INTO photo VALUES (1);
INSERT INTO comment (post_id, body) VALUES (1, 'nice post');
""")
for sql in ["INSERT INTO comment (post_id, photo_id, body) VALUES (1, 1, 'two parents')",
            "INSERT INTO comment (post_id, body) VALUES (77, 'ghost post')",
            "INSERT INTO comment (body) VALUES ('orphan')"]:
    try:
        db.execute(sql); print("accepted:", sql[:44])
    except sqlite3.IntegrityError as e:
        print("blocked :", e)''')
body=f'''
<h2 id="x11-6-modelling-extras-fd-closure-bcnf-by-algorithm-and-patterns-you-will-meet">11.6 Modelling Extras: Functional-Dependency Closure, BCNF by Algorithm, and Patterns You Will Meet</h2>
{co("blue","INTUITION","Section 11.2 found normalization problems by eye. Eyes miss things in a table with twelve columns. Database theory gives a mechanical test: write the rules of the data as <strong>functional dependencies</strong> (FDs), compute what each column set determines (its <strong>closure</strong>), and read off the keys and the violations. Then you decompose by algorithm, and prove with a query that nothing was lost.")}
<h3>Words you need</h3>
<ul><li><strong>Functional dependency</strong> <code>X -&gt; Y</code>: whenever two rows agree on X they must agree on Y. 'course -&gt; teacher' says each course has one teacher.</li><li><strong>Closure</strong> of a set X, written X<sup>+</sup>: every column determined by X, found by applying the FDs again and again.</li><li><strong>Superkey</strong>: a column set whose closure is all columns. A <strong>candidate key</strong> is a minimal superkey.</li><li><strong>BCNF</strong>: every FD <code>X -&gt; Y</code> has a superkey on the left. Any FD that breaks this is a violation.</li></ul>
{P("11.6.1","A table <code>enrol(student, course, grade, teacher, office)</code> has the rules: (student, course) -&gt; grade, course -&gt; teacher, teacher -&gt; office. Find the candidate key and the BCNF violations. Predict first: the key is (student, course), and both <code>course -&gt; teacher</code> and <code>teacher -&gt; office</code> violate BCNF.")}
{py(fd)}
{text(fdo)}
{steps([("Step 1","Closure of {course}: start with course. Rule 2 adds teacher. Rule 3 then adds office. Nothing else applies: {course, office, teacher}. It is missing student and grade, so course alone is not a key."),("Step 2","Closure of {student, course}: rule 1 adds grade, rule 2 teacher, rule 3 office. That is all five columns, so it is a key, and it is minimal because neither student nor course alone reaches everything."),("Step 3","Check each rule's left side. (student, course) is a superkey, so rule 1 is fine. course is not, so <code>course -&gt; teacher</code> violates BCNF. teacher is not, so <code>teacher -&gt; office</code> violates too."),("Meaning","The violations are exactly the redundancy you would see: the office of 'Iyer' is repeated for every enrolment of every course Iyer teaches, and an office change has to be made in several rows.")])}
<h3>The decomposition algorithm and the lossless check</h3>
<p>Pick a violating FD X -&gt; Y. Split the table into (X plus Y) and (everything except Y, which keeps X). Repeat on each piece until none violates. Here: split on <code>teacher -&gt; office</code> first (teacher_office), then <code>course -&gt; teacher</code> (course_teacher), leaving (student, course, grade). Because each split keeps the determinant X as the join column, the pieces rejoin exactly. The code builds the three tables and proves it:</p>
{py(dec)}
{text(deco)}
{steps([("Step 1","Three small tables, each with a key that is the left side of its FD."),("Step 2","Joining them back gives the same 5 rows as the original: a <strong>lossless</strong> decomposition."),("Step 3","The office of Iyer now lives in one row. One <code>UPDATE</code> changed it for both Stats and ML. In the original table you would have had to update 3 rows and could easily miss one.")])}
{co("red","COMMON MISTAKE","Splitting a table into two pieces that share no determining column, for example (student, grade) and (course, teacher). Joining them back on nothing, or on a non-key column, creates <em>spurious rows</em> that never existed. A decomposition is only safe when the shared columns form a key of at least one piece, which is exactly what the algorithm guarantees.")}
{co("green","GOING DEEPER","BCNF can lose a dependency: some decompositions mean an FD can no longer be checked inside one table, which is why many designers stop at 3NF, which always preserves dependencies. 4NF goes one step further for multi-valued facts: if a person has independent sets of skills and languages, one table of (person, skill, language) must list every combination, and the fix is two tables (person, skill) and (person, language). In practice: aim for 3NF in transactional systems, check by FD closure when a design feels wrong, and denormalize deliberately (Section 11.3) only in analytics layers.")}
<h3>Pattern 1: soft delete without breaking uniqueness</h3>
<p>Soft delete means marking a row deleted (<code>deleted_at</code>) instead of removing it, so history survives and mistakes can be undone. The trap: a normal <code>UNIQUE (email)</code> blocks a person who deleted their account from signing up again. A <strong>partial unique index</strong> enforces uniqueness only among live rows.</p>
{sd}
{steps([("Step 1","Row 1 is soft-deleted, so the live-only index ignores it, and a second row with the same email is accepted."),("Step 2","A third insert would create two <em>live</em> rows with that email, and the index rejects it."),("Note","Every query must now remember <code>WHERE deleted_at IS NULL</code>. Hide that behind a view (<code>CREATE VIEW live_users AS ...</code>), or the first forgotten filter shows deleted data. In PostgreSQL row-level security can enforce it.")])}
<h3>Pattern 2: multi-tenant design that cannot cross tenants</h3>
<p>In a SaaS product many customers (tenants) share tables. The worst bug is one tenant seeing another's data. Put <code>tenant_id</code> in every key, and make foreign keys include it, so the database itself refuses a cross-tenant reference.</p>
{mt}
{steps([("Step 1","The primary key of <code>customer</code> is (tenant_id, customer_id). Both tenants have a customer 10, which is fine."),("Step 2","The foreign key in <code>orders</code> is composite. A tenant-1 order can only point to a (1, customer) pair that exists, so a typo or an attack that points at tenant 2's customer is refused."),("Step 3","The failing insert shows the database error. Add row-level security (Section 9.6) so queries are also filtered by tenant.")])}
<h3>Pattern 3: polymorphic references, done safely</h3>
<p>Comments that can belong to a post <em>or</em> a photo are often stored as <code>(target_type, target_id)</code>. That cannot have a foreign key, so orphans creep in. A safe design uses one nullable foreign key per parent and a <code>CHECK</code> that exactly one is set:</p>
{po}
{steps([("Step 1","Two parents set: the <code>CHECK</code> rejects it."),("Step 2","A post that does not exist: the foreign key rejects it."),("Step 3","No parent at all: the <code>CHECK</code> rejects it. The two-column design needs a new column per new parent type, but the database now guards every row.")])}
<h3>Surrogate versus natural keys, and where this meets data engineering</h3>
<p>A <strong>natural key</strong> comes from the real world (email, ISBN); a <strong>surrogate key</strong> is a meaningless number the database hands out. Natural keys change (people change email) and cost more to join on, so use a surrogate primary key and keep a <code>UNIQUE</code> constraint on the natural one, as Section 9.1 advised. For many-to-many relations the junction table's key is the pair of foreign keys. In a warehouse the same ideas reappear as layers: raw tables as loaded, staging models that rename and clean, and mart models shaped as stars. <strong>Data Vault</strong> is a warehouse modelling style that separates stable business keys (hubs), relationships (links) and changing attributes (satellites) so history is never rewritten; it suits many source systems, and costs more joins. A tool such as dbt expresses each layer as a SQL model (see the Data Engineering document).</p>
<h3>Practice with answers</h3>
{qa("11.6.2","Given R(a, b, c) with FDs a -&gt; b and b -&gt; c, what is the closure of {a} and is a the key? <em>(easy)</em>","a determines b, b then determines c, so the closure is {a, b, c}: all columns. a is a key. The FD b -&gt; c violates BCNF (b is not a key), but it is a transitive dependency, so it also violates 3NF.")}
{qa("11.6.3","Decompose R(a, b, c) from the previous problem. <em>(medium)</em>","Split on b -&gt; c: R1(b, c) with key b, and R2(a, b) with key a. They share b, which is a key of R1, so the join is lossless.")}
{qa("11.6.4","Why does <code>UNIQUE (email)</code> plus soft delete cause trouble, and give two fixes. <em>(find the bug)</em>","A deleted row keeps its email, so the person cannot register again. Fix 1: a partial unique index where <code>deleted_at IS NULL</code> (PostgreSQL, SQLite). Fix 2: on deletion, rewrite the email to a unique tombstone, or move the row to an archive table. MySQL has no partial indexes, so use the second or a generated column.")}
{qa("11.6.5","Why should every table in a multi-tenant database include tenant_id in its primary key and foreign keys? <em>(interview)</em>","So the schema itself prevents cross-tenant references and makes per-tenant queries and sharding natural; a plain integer key would let a bug link tenant 1 to tenant 2's data, which is a data-leak class of defect. It costs a wider index and slightly larger keys.")}
'''
insert("11","lab11",body)
