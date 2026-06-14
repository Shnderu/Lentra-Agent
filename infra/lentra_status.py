import psycopg2

conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

cur = conn.cursor()

print("\n=== LENTRA STATUS ===\n")

cur.execute("""
SELECT status, COUNT(*)
FROM processing_queue
GROUP BY status
ORDER BY status;
""")

print("[QUEUE]")
for row in cur.fetchall():
    print(row)

cur.execute("""
SELECT COUNT(*)
FROM processing_queue
WHERE delivered IS NULL
AND status='done';
""")

print("\n[PENDING DELIVERY]")
print(cur.fetchone()[0])

cur.execute("""
SELECT COUNT(*)
FROM processing_queue
WHERE status='error';
""")

print("\n[ERROR TASKS]")
print(cur.fetchone()[0])

cur.close()
conn.close()

print("\n====================\n")
