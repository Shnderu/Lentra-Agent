from flask import Flask, Response
import psycopg2
import os

app = Flask(__name__)

DB = {
    "host": os.getenv("DB_HOST", "db"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


@app.route("/metrics")
def metrics():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    cur.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
    rows = cur.fetchall()

    conn.close()

    out = []
    for r in rows:
        out.append(f"tasks_status{{status=\"{r[0]}\"}} {r[1]}")

    return Response("\n".join(out), mimetype="text/plain")
