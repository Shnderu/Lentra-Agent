import json
import time
import redis

"""
Lentra Stability Layer v3
SELF HEALING ENGINE (SAFE MODE)
- does NOT auto-fix anything destructive
- only controlled patch suggestions
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_SUGGESTIONS = "stream:system:suggestions"
STREAM_HEALTH = "stream:system:health"


def evaluate(suggestion):
    fixes = []

    for fix in suggestion.get("suggested_fixes", []):
        if "redis" in fix:
            fixes.append({
                "type": "CONFIG",
                "action": "CHECK_REDIS_RETRY_POLICY",
                "risk": "LOW"
            })

        if "worker" in fix:
            fixes.append({
                "type": "OBSERVABILITY",
                "action": "ENABLE_WORKER_HEARTBEAT",
                "risk": "LOW"
            })

        if "pipeline" in fix:
            fixes.append({
                "type": "ARCHITECTURE",
                "action": "ISOLATE_EXECUTION_LAYER",
                "risk": "MEDIUM"
            })

    return fixes


def run():
    print(">>> SELF HEALING ENGINE STARTED")

    last_id = "0"

    while True:
        try:
            resp = r.xread({STREAM_SUGGESTIONS: last_id}, block=5000, count=10)

            if not resp:
                continue

            for stream, messages in resp:
                for msg_id, msg in messages:
                    last_id = msg_id

                    print(">>> SUGGESTION RECEIVED:", msg)

                    parsed = msg
                    fixes = evaluate(parsed)

                    payload = {
                        "source_id": msg_id,
                        "fixes": fixes,
                        "timestamp": time.time(),
                        "applied": False,
                        "mode": "SAFE_ONLY"
                    }

                    r.xadd(STREAM_HEALTH, payload)

                    print(">>> FIX PLAN:", json.dumps(payload, indent=2))

        except Exception as e:
            print("[SELF HEAL ERROR]", e)
            time.sleep(3)


if __name__ == "__main__":
    run()
