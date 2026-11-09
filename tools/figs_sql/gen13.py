from _kit import *
db=sqlite3.connect(":memory:",isolation_level=None)
X=lambda c: exec_sql(db,c)
emb=X("""CREATE TABLE doc_orders (id INTEGER PRIMARY KEY, doc TEXT);
INSERT INTO doc_orders VALUES
 (1, '{"customer": {"name": "Asha", "city": "Pune"}, "items": [{"sku": "kb", "qty": 1}, {"sku": "nb", "qty": 2}]}'),
 (2, '{"customer": {"name": "Asha", "city": "Pune"}, "items": [{"sku": "dl", "qty": 1}]}'),
 (3, '{"customer": {"name": "Ravi", "city": "Mumbai"}, "items": [{"sku": "ms", "qty": 1}]}');
SELECT json_extract(doc, '$.customer.name') AS customer, sum(json_extract(j.value, '$.qty')) AS units
FROM doc_orders, json_each(doc, '$.items') AS j
GROUP BY customer ORDER BY customer;""")
upd=X("""UPDATE doc_orders SET doc = json_set(doc, '$.customer.city', 'Mumbai') WHERE id = 1;
SELECT id, json_extract(doc, '$.customer.name') AS name, json_extract(doc, '$.customer.city') AS city FROM doc_orders ORDER BY id;""")
rep='''import random
random.seed(3)

class Replica:
    def __init__(self):
        self.data = {}

primary, follower = Replica(), Replica()
pending = []                                  # writes still travelling to the follower

def write(key, value):
    primary.data[key] = value
    pending.append((key, value))              # replicated later, not instantly

def replicate_some():
    while pending and random.random() < 0.5:  # the network delivers some writes per tick
        k, v = pending.pop(0)
        follower.data[k] = v

write("profile:7", "new name")
print("read from follower right after the write :", follower.data.get("profile:7"))
replicate_some(); replicate_some(); replicate_some()
print("read from follower a few ticks later      :", follower.data.get("profile:7"))

# fix 1: read your own writes. After a write, read from the primary for a while.
write("profile:8", "x")
print("read-your-writes (primary) right after    :", primary.data.get("profile:8"))
'''
repo=pyrun(rep)
part='''from collections import Counter
# 1 million readings from 1,000 sensors, one reading per second for ~17 minutes each
sensors, seconds = 1000, 1000
rows_by_sensor = Counter()
for s in range(sensors):
    for t in range(seconds):
        rows_by_sensor[s] += 1
print("partition = sensor      : %d partitions, %d rows each" % (len(rows_by_sensor), max(rows_by_sensor.values())))

# at full speed one sensor makes 86,400 rows a day, 31.5 million a year
per_year = 86400 * 365
print("one sensor, one year    : %d rows in a single partition" % per_year)
print("partition = sensor+day  : %d rows per partition, %d partitions per sensor-year" % (86400, 365))
'''
parto=pyrun(part)
fof=X("""CREATE TABLE friend (a INTEGER, b INTEGER);
INSERT INTO friend VALUES (1,2),(2,1),(1,3),(3,1),(2,4),(4,2),(3,4),(4,3),(4,5),(5,4),(5,6),(6,5);
SELECT DISTINCT f2.b AS suggestion
FROM friend f1 JOIN friend f2 ON f2.a = f1.b
WHERE f1.a = 1 AND f2.b <> 1 AND f2.b NOT IN (SELECT b FROM friend WHERE a = 1)
ORDER BY suggestion;""")
body=f'''
<h2 id="x13-8-modelling-for-nosql-embed-or-reference-partition-keys-lag-and-friend-graphs">13.8 Modelling for NoSQL: Embed or Reference, Partition Keys, Replica Lag and Friend Graphs</h2>
{co("blue","INTUITION","In SQL you model the <em>facts</em> and let queries combine them. In most NoSQL stores you model the <em>queries</em>: you list the questions the application will ask, then shape the data so each question is a single fast lookup. That is why the same shop is designed differently in a document store, a wide-column store and a graph, and why it can be painful when a new question appears. These examples show the design moves, with runnable stand-ins where a real server is not available. MongoDB, Redis, Cassandra and Neo4j commands are labelled <em>not run here</em>.")}
<h3>Example 1: embed or reference in a document store</h3>
<p>An order has a customer and a list of items. In MongoDB you either <strong>embed</strong> the customer and items inside the order document, or <strong>reference</strong> them by id and look them up in another collection. Embedding makes reads one lookup and writes atomic; referencing avoids copying data that changes. SQLite's JSON functions let us feel the difference with real output:</p>
{P("13.8.1","Store three orders as JSON documents with the customer embedded, then count units per customer. Predict first: Asha has 3 + 1 = 4 units (two orders), Ravi 1.")}
{emb}
{steps([("Step 1","Each document is self-contained: one read returns the order, the customer and the items. That is the speed benefit of embedding."),("Step 2","The query walks each document's item array with <code>json_each</code> and sums quantities per customer name. Asha 4 units (1 + 2 + 1), Ravi 1."),("Meaning","MongoDB's equivalent is an aggregation pipeline with <code>$unwind</code> and <code>$group</code> (not run here).")])}
<p>Now the price of embedding. Asha moves to Mumbai and we update <em>one</em> order document, as an application that forgot about the copies would:</p>
{upd}
{steps([("Step 1","Order 1 now says Mumbai, order 2 still says Pune. The same customer has two cities: an update anomaly, exactly like the one normalization removes (Chapter 11)."),("Step 2","In a document store you accept this when the copy is meant to be a <em>snapshot</em>. An order should record the address it was shipped to, so the old city is correct for order 2."),("Rule","Embed data that is read together and does not change independently or is a historical snapshot (order lines, shipping address). Reference data that changes in one place and is shared (customer profile, product price now).")])}
{co("red","COMMON MISTAKE","Embedding an unbounded list, such as every comment ever made inside the post document. Documents have a size limit (16 MB in MongoDB) and grow slowly into a performance problem, because every update rewrites a larger document. Reference unbounded children in their own collection.")}
<h3>Example 2: choosing a partition key (Cassandra, DynamoDB)</h3>
<p>In wide-column stores the <strong>partition key</strong> decides which machine holds a row and how much data one partition contains. Rows with the same key sit together and are read together fast, but one giant partition becomes a hot spot. For sensor data the natural key is the sensor, which is wrong at scale. The numbers show why:</p>
{P("13.8.2","One sensor writes one reading per second. Compare 'partition by sensor' with 'partition by sensor and day'. Predict first: a year is 31.5 million rows per partition against 86,400.")}
{py(part)}
{text(parto)}
{steps([("Step 1","With the key (sensor) a year of data for one sensor sits in a single partition of 31,536,000 rows. Cassandra recommends keeping partitions well below 100 MB, and this one would be far over."),("Step 2","Adding the day to the key caps a partition at 86,400 rows. Reading one day is one partition; reading a week is 7 partition reads, still cheap."),("Step 3","The CQL shape is <code>PRIMARY KEY ((sensor_id, day), ts)</code>: the double brackets mean 'partition key is the pair', and <code>ts</code> orders rows inside the partition (not run here)."),("Rule","Choose a key that spreads data evenly <em>and</em> lets your main query hit one or a few partitions. Never one that grows without bound.")])}
<h3>Example 3: replica lag, and reading your own writes</h3>
<p>Most distributed stores copy each write to several machines and acknowledge before all copies have it. A reader hitting a lagging copy sees old data. This is <strong>eventual consistency</strong>. A tiny simulation with a seeded random network shows the symptom and one standard fix:</p>
{py(rep)}
{text(repo)}
{steps([("Step 1","The write reaches the primary at once. The follower has not received it, so reading the follower returns <code>None</code>: the user saves their profile and sees the old one."),("Step 2","A few ticks later the follower has caught up. 'Eventually' means exactly that: the copies agree if you wait."),("Step 3","Fix: <strong>read your own writes</strong>. For a short time after a user writes, send that user's reads to the primary (or use a session token that records the version the user has written). Other users can tolerate staleness."),("Meaning","Consistency is not all or nothing. Decide per feature: a bank balance needs the latest value, a like counter does not.")])}
<h3>Example 4: friends of friends, in SQL and in Cypher</h3>
<p>Graph databases shine at 'who is within two hops'. The SQL version is a self-join, which grows more expensive with each extra hop. A small friendship table (edges stored both ways) and the query to suggest friends to user 1, people two hops away who are not already friends:</p>
{fof}
{steps([("Step 1","User 1's friends are 2 and 3. Friends of 2 are 1 and 4. Friends of 3 are 1 and 4."),("Step 2","Remove user 1 and anyone who is already a friend. What remains is user 4 (friend of both 2 and 3) as the single suggestion. User 5 is three hops away, so it is excluded."),("Cypher","In Neo4j the same query is <code>MATCH (me:User {id: 1})-[:FRIEND]-&gt;()-[:FRIEND]-&gt;(s) WHERE NOT (me)-[:FRIEND]-(s) AND s &lt;&gt; me RETURN DISTINCT s</code> (not run here). Adding a third hop is one more arrow, while SQL needs another join.")])}
<h3>SQL or NoSQL? A decision table</h3>
{tbl(["Situation","Good first choice","Why"],[
["Orders, payments, inventory with relationships and transactions","PostgreSQL or another relational database","joins, constraints and ACID are what the problem needs"],
["Product catalogue where each item has different attributes","PostgreSQL with <code>jsonb</code>, or a document store","flexible shape with a relational core"],
["Session data, caches, rate limits, leaderboards","Redis","in-memory speed, TTL, sorted sets"],
["Billions of time-stamped events, simple read patterns","Cassandra, or a time-series or columnar engine","write throughput, partitioned by time"],
["Deep relationship queries (recommendations, fraud rings)","graph database, or recursive SQL at small scale","hops are cheap in a graph"],
["Full-text search and similarity search","search engine or vector index","ranking and approximate matching"]])}
<p>The honest default for a new product is a relational database. Reach for a specialised store when you can name the specific query or scale that a relational database cannot serve, and keep the relational one as the source of truth.</p>
<h3>Practice with answers</h3>
{qa("13.8.3","An e-commerce order document embeds the product's current price. The price changes. Is that a bug? <em>(medium)</em>","No, it is the desired snapshot: the order should keep the price the customer paid. The bug would be showing the live product price on an old invoice. Embed price at purchase, reference the product id for the current catalogue.")}
{qa("13.8.4","A table is partitioned by country and 40 percent of users are in one country. Problem? <em>(medium)</em>","A hot partition: one machine takes 40 percent of the traffic and storage, so scaling out does not help. Add a second key part (hash bucket, month, or user id range) so rows spread more evenly.")}
{qa("13.8.5","A user posts a comment and refreshes; the comment is missing for two seconds. Cause and fix? <em>(interview)</em>","Replica lag: the read went to a follower that had not received the write. Fix: read your own writes (route that user's reads to the primary for a short window, or use a session token / quorum read). Not every read needs it.")}
{qa("13.8.6","Why can friends-of-friends be slow in SQL on a large network and fast in a graph database? <em>(expert)</em>","SQL answers each hop with a join over the whole edge table (an index lookup per row, with intermediate results growing quickly). A native graph store keeps each node's neighbours next to it (index-free adjacency), so a hop follows pointers whose cost depends on the number of neighbours, not the table size. At small scale with an index on (a), SQL is fine.")}
'''
insert("13","lab13",body)
