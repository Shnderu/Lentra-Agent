from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DB = {
    "host": "db",
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}

@app.route("/health")
def health():
    try:
        conn = psycopg2.connect(**DB)
        cur = conn.cursor()

        cur.execute("SELECT 1")
        db_ok = cur.fetchone()[0] == 1

        return jsonify({
            "db": db_ok,
            "status": "ok"
        })

    except Exception as e:
        return jsonify({
            "status": "fail",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
