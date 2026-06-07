import datetime
import os
import psycopg2
import subprocess
from pathlib import Path


STATE_FILE = "/app/docs/STATE.md"


# ----------------------------
# Docker layer (soft observability)
# ----------------------------
def docker_ps():
    try:
        result = subprocess.check_output(
            ["docker", "ps", "--format", "{{.Names}}|{{.Status}}"]
        ).decode()

        containers = {}
        for line in result.strip().split("\n"):
            if "|" in line:
                name, status = line.split("|", 1)
                containers[name] = status

        return {"status": "ok", "data": containers}

    except Exception as e:
        return {"status": "unavailable", "error": str(e)}


# ----------------------------
# DB + queue metrics (REAL SOURCE OF TRUTH)
# ----------------------------
def db_metrics():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "readme_to_recover"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
        )
        conn.autocommit = True

        with conn.cursor() as cur:

            # queue distribution
            cur.execute("""
                SELECT status, COUNT(*)
                FROM tasks
                GROUP BY status;
            """)
            rows = cur.fetchall()

            metrics = {
                "pending": 0,
                "processing": 0,
                "done": 0,
                "failed": 0
            }

            for status, count in rows:
                metrics[status] = count

        conn.close()

        return {
            "status": "ok",
            "metrics": metrics
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


# ----------------------------
# Worker runtime metrics (lightweight local telemetry)
# ----------------------------
def worker_metrics():
    # пока без persistent storage — позже вынесем в Redis
    return {
        "processed": 0,
        "failed": 0,
        "idle": True
    }


# ----------------------------
# STATE writer
# ----------------------------
def write_state():
    docker = docker_ps()
    db = db_metrics()
    worker = worker_metrics()

    now = datetime.datetime.utcnow().isoformat()

    lines = []
    lines.append("# FlyRum STATE (v4 - runtime contract)")
    lines.append(f"\nGenerated: {now}\n")

    # ---------------- Infrastructure ----------------
    lines.append("## Infrastructure")

    if docker["status"] == "ok":
        for k, v in docker["data"].items():
            lines.append(f"- {k} : {v}")
    else:
        lines.append(f"- docker : unavailable ({docker['error']})")

    # ---------------- Queue ----------------
    lines.append("\n## Queue Metrics")

    if db["status"] == "ok":
        m = db["metrics"]
        lines.append(f"- pending : {m['pending']}")
        lines.append(f"- processing : {m['processing']}")
        lines.append(f"- done : {m['done']}")
        lines.append(f"- failed : {m['failed']}")
    else:
        lines.append(f"- error : {db['error']}")

    # ---------------- Worker ----------------
    lines.append("\n## Worker Metrics")
    lines.append(f"- processed : {worker['processed']}")
    lines.append(f"- failed : {worker['failed']}")
    lines.append(f"- idle : {worker['idle']}")

    # ---------------- Runtime ----------------
    lines.append("\n## Runtime Signals")
    lines.append(f"- heartbeat : {now}")

    Path("/app/docs").mkdir(parents=True, exist_ok=True)

    with open(STATE_FILE, "w") as f:
        f.write("\n".join(lines))

    print("STATE updated (v4 runtime contract)")


if __name__ == "__main__":
    write_state()
