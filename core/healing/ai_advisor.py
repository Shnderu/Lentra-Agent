import redis
import json
from collections import Counter

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)


def load_events(limit=200):
    data = r.xrevrange("stream:telemetry", "+", "-", count=limit)
    return [e[1] for e in data] if data else []


def detect_patterns(events):
    errors = [e for e in events if e.get("type") == "task.error"]
    success = [e for e in events if e.get("type") == "task.success"]

    stages = Counter([e.get("stage", "unknown") for e in errors])
    error_types = Counter([e.get("error_type", "unknown") for e in errors])

    return {
        "error_count": len(errors),
        "success_count": len(success),
        "stage_distribution": dict(stages),
        "error_types": dict(error_types),
        "health_ratio": (len(success) / (len(success) + len(errors) + 1e-9))
    }


def infer_root_cause(analysis):
    # deterministic inference layer (NOT LLM)
    if analysis["error_count"] == 0:
        return "NO_FAILURES"

    top_stage = max(analysis["stage_distribution"].items(), key=lambda x: x[1])[0] if analysis["stage_distribution"] else "unknown"

    top_error = None
    if analysis["error_types"]:
        top_error = max(analysis["error_types"].items(), key=lambda x: x[1])[0]

    if top_error == "TimeoutError":
        return "INFRA_LATENCY_OR_IO_BOTTLENECK"

    if top_error == "ConnectionError":
        return "NETWORK_OR_REDIS_CONNECTIVITY_ISSUE"

    return f"ISSUES_IN_{top_stage}"


def suggest_fixes(root_cause):
    fixes = []

    if root_cause == "INFRA_LATENCY_OR_IO_BOTTLENECK":
        fixes.append("increase redis xreadgroup block timeout")
        fixes.append("add retry backoff jitter")

    if root_cause == "NETWORK_OR_REDIS_CONNECTIVITY_ISSUE":
        fixes.append("check docker network binding (infra_default)")
        fixes.append("verify service DNS resolution")

    if "worker" in root_cause:
        fixes.append("restart worker container (safe action)")

    if not fixes:
        fixes.append("no safe automated fix available")

    return fixes


def run():
    events = load_events()

    analysis = detect_patterns(events)
    root_cause = infer_root_cause(analysis)
    fixes = suggest_fixes(root_cause)

    report = {
        "status": "SAFE_AI_ADVISOR",
        "root_cause": root_cause,
        "analysis": analysis,
        "suggested_fixes": fixes,
        "mode": "SUGGEST_ONLY",
        "safety": {
            "auto_apply": False,
            "risk_level": "CONTROLLED"
        }
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()
