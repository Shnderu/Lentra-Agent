from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DB = {
    "host": os.getenv("DB_HOST", "db"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

@app.route("/status")
def status():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    cur.execute("SELECT status, COUNT(*) FROM workflow_tasks GROUP BY status")
    data = cur.fetchall()

    conn.close()

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
