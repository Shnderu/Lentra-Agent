import redis
import json

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)


def analyze():
    events = r.xrange("stream:telemetry", "-", "+", count=200)

    errors = []
    successes = []

    for _, e in events:
        if e.get("type") == "task.error":
            errors.append(e)
        if e.get("type") == "task.success":
            successes.append(e)

    if not errors:
        return {
            "status": "OK",
            "root_cause": "NO_FAILURES",
            "message": "System healthy"
        }

    # simple clustering by stage
    by_stage = {}
    for e in errors:
        stage = e.get("stage", "unknown")
        by_stage.setdefault(stage, 0)
        by_stage[stage] += 1

    worst_stage = max(by_stage.items(), key=lambda x: x[1])[0]

    return {
        "status": "FAILURE_CLUSTER",
        "root_cause": f"ISSUES_IN_{worst_stage}",
        "error_count": len(errors),
        "stage_distribution": by_stage,
        "note": "first deterministic RCA layer"
    }


if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
