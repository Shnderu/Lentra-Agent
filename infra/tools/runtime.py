# ============================================================
# LENTRA RUNTIME DASHBOARD V1
# ============================================================

import os
import sys
import json
import psycopg2
from datetime import datetime

from lentra.observability.service import ObservabilityService
from lentra.telegram.delivery.consumer import get_conn


obs = ObservabilityService()


# ============================================================
# DB SNAPSHOT
# ============================================================

def get_db_snapshot(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT status, COUNT(*)
        FROM processing_queue
        GROUP BY status
    """)

    rows = cur.fetchall()

    data = {r[0]: r[1] for r in rows}

    return {
        "pending": data.get("pending", 0),
        "processing": data.get("processing", 0),
        "delivered": data.get("delivered", 0),
        "failed": data.get("failed", 0),
    }


# ============================================================
# SYSTEM SNAPSHOT
# ============================================================

def get_system_snapshot():
    return obs.get_system_snapshot()


# ============================================================
# LAST TRACE INSPECTOR (IN-MEMORY ONLY)
# ============================================================

def get_traces():
    traces = obs.traces

    result = []

    for trace_id, trace in list(traces.items())[-10:]:
        last_stage = trace.events[-1].stage if trace.events else None

        result.append({
            "trace_id": trace_id,
            "events": len(trace.events),
            "last_stage": last_stage
        })

    return result


# ============================================================
# MAIN DASHBOARD
# ============================================================

def main():

    print("\n==============================")
    print(" LENTRA RUNTIME DASHBOARD V1")
    print("==============================\n")

    # ---------------- SYSTEM ----------------
    system = get_system_snapshot()

    print("[SYSTEM]")
    print(json.dumps(system, indent=2))
    print()

    # ---------------- DB ----------------
    try:
        conn = get_conn()
        db = get_db_snapshot(conn)

        print("[QUEUE]")
        print(json.dumps(db, indent=2))
        print()

    except Exception as e:
        print("[QUEUE ERROR]", str(e))
        print()

    # ---------------- TRACES ----------------
    traces = get_traces()

    print("[LAST TRACES]")
    print(json.dumps(traces, indent=2))
    print()

    # ---------------- SUMMARY ----------------
    print("[STATUS SUMMARY]")

    if db.get("processing", 0) > 5:
        print("⚠️  CONSUMER POSSIBLE LAG")

    if db.get("pending", 0) > 0:
        print("⚠️  QUEUE BACKLOG")

    if system.get("metrics", {}).get("requests", 0) == 0:
        print("⚠️  NO TRAFFIC")

    print("\n==============================\n")


if __name__ == "__main__":
    main()
