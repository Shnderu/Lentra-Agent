import json
import time
import redis

"""
Lentra Stability Layer v3
SAFE AI ADVISOR (read-only + suggestion engine)
"""

REDIS_HOST = "lentra-redis"
REDIS_PORT = 6379

STREAM_ERRORS = "stream:system:errors"
STREAM_HEALTH = "stream:system:health"
STREAM_SUGGESTIONS = "stream:system:suggestions"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def analyze_system():
    error_count = 0
    success_count = 0
    error_types = {}

    try:
        # ошибки системы (если есть)
        errors = r.xrange(STREAM_ERRORS, min="-", max="+", count=100)

        for _, msg in errors:
            error_count += 1
            etype = msg.get("type", "unknown")
            error_types[etype] = error_types.get(etype, 0) + 1

        results = r.xrange("stream:rent:results", "-", "+", count=200)
        success_count = len(results)

    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e)
        }

    health_ratio = success_count / max(success_count + error_count, 1)

    return {
        "status": "SAFE_AI_ADVISOR",
        "analysis": {
            "error_count": error_count,
            "success_count": success_count,
            "error_types": error_types,
            "health_ratio": health_ratio
        }
    }


def generate_suggestions(analysis: dict):
    suggestions = []

    if analysis["analysis"]["error_count"] > 0:
        suggestions.append("add retry backoff on redis xreadgroup")
        suggestions.append("add worker heartbeat monitoring")

    if analysis["analysis"]["health_ratio"] < 0.5:
        suggestions.append("pipeline instability detected - isolate worker execution layer")

    if not suggestions:
        suggestions.append("system stable - no action required")

    return suggestions


def run():
    print(">>> SAFE AI ADVISOR STARTED")

    while True:
        data = analyze_system()

        if data["status"] == "ERROR":
            print(data)
            time.sleep(5)
            continue

        suggestions = generate_suggestions(data)

        payload = {
            "ts": time.time(),
            "analysis": data,
            "suggested_fixes": suggestions,
            "mode": "SUGGEST_ONLY",
            "safety": {
                "auto_apply": False,
                "risk_level": "CONTROLLED"
            }
        }

        print(json.dumps(payload, indent=2))

        try:
            r.xadd(STREAM_SUGGESTIONS, payload)
        except Exception as e:
            print("[REDIS ERROR]", e)

        time.sleep(10)


if __name__ == "__main__":
    run()
