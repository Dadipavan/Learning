"""Shared tiny shop database used by the SQL figures and the SQL sections (same data as chapter 6)."""
import sqlite3
def make():
    con = sqlite3.connect(":memory:")
    con.executescript("""
CREATE TABLE customers(cust_id INT, name TEXT, city TEXT, signup_date TEXT);
INSERT INTO customers VALUES
 (1,'Asha','Pune','2025-01-05'),(2,'Ravi','Delhi','2025-01-20'),
 (3,'Meera','Pune','2025-02-03'),(4,'Imran','Mumbai','2025-02-14'),
 (5,'Kavya','Delhi','2025-03-01'),(6,'Dev','Mumbai','2025-03-10');
CREATE TABLE orders(order_id INT, cust_id INT, order_date TEXT, amount REAL, status TEXT);
INSERT INTO orders VALUES
 (1,1,'2025-01-06',1200,'delivered'),(2,1,'2025-01-25',800,'delivered'),
 (3,2,'2025-01-22',1500,'delivered'),(4,3,'2025-02-04',500,'returned'),
 (5,3,'2025-02-20',900,'delivered'),(6,1,'2025-02-11',2000,'delivered'),
 (7,4,'2025-02-15',700,'delivered'),(8,2,'2025-03-02',1100,'delivered'),
 (9,5,'2025-03-03',NULL,'pending'),(10,4,'2025-03-12',1300,'delivered'),
 (11,1,'2025-03-15',600,'delivered'),(12,5,'2025-03-20',2500,'delivered'),
 (13,3,'2025-03-22',400,'cancelled'),(14,2,'2025-04-02',1700,'delivered');
""")
    return con
