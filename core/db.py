import psycopg2

conn = psycopg2.connect(
    host="flyrum_db",
    database="flyrum",
    user="postgres",
    password="postgres"
)

conn.autocommit = True
