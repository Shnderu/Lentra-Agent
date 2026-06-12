import json
import redis
import traceback
import time
import socket
from dataclasses import dataclass, asdict
from typing import Dict, Any, List


@dataclass
class HealthReport:
    status: str
    root_cause: str
    severity: str
    stage: str
    metrics: Dict[str, Any]
    analysis: Dict[str, Any]
    suggestions: List[str]
    safety: Dict[str, Any]


class SafeAIAdvisor:
    """
    SAFE MODE ONLY:
    - No writes
    - No auto-fix
    - No system mutation
    """

    def __init__(self, redis_host="lentra-redis", redis_port=6379):
        self.redis_host = redis_host
        self.redis_port = redis_port

    def _check_redis(self):
        try:
            r = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                decode_responses=True,
                socket_connect_timeout=2
            )
            return {
                "status": "ok",
                "ping": r.ping()
            }
        except Exception as e:
            return {
                "status": "fail",
                "error": str(e),
                "trace": traceback.format_exc()
            }

    def _check_dns(self):
        try:
            socket.gethostbyname(self.redis_host)
            return {"status": "ok"}
        except Exception as e:
            return {"status": "fail", "error": str(e)}

    def analyze_pipeline(self) -> HealthReport:
        redis_check = self._check_redis()
        dns_check = self._check_dns()

        metrics = {
            "redis": redis_check,
            "dns": dns_check,
            "timestamp": time.time()
        }

        # ROOT CAUSE CLASSIFICATION (NO EXECUTION)
        if redis_check["status"] == "fail":
            if "Name or service not known" in redis_check.get("error", ""):
                root_cause = "DNS_RESOLUTION_FAILURE"
            elif "timeout" in redis_check.get("error", "").lower():
                root_cause = "REDIS_TIMEOUT"
            else:
                root_cause = "REDIS_CONNECTION_FAILURE"
        else:
            root_cause = "NO_FAILURES"

        suggestions = []

        if root_cause == "DNS_RESOLUTION_FAILURE":
            suggestions.append("Check docker network attachment (worker -> infra_default)")
            suggestions.append("Verify service name 'lentra-redis' in docker DNS")
        elif root_cause == "REDIS_TIMEOUT":
            suggestions.append("Increase socket_connect_timeout")
            suggestions.append("Check Redis CPU/IO saturation")
        elif root_cause == "REDIS_CONNECTION_FAILURE":
            suggestions.append("Verify Redis container health and port binding")

        return HealthReport(
            status="SAFE_AI_ADVISOR",
            root_cause=root_cause,
            severity="HIGH" if root_cause != "NO_FAILURES" else "LOW",
            stage="PIPELINE_ANALYSIS",
            metrics=metrics,
            analysis={
                "redis_status": redis_check["status"],
                "dns_status": dns_check["status"]
            },
            suggestions=suggestions,
            safety={
                "auto_apply": False,
                "mode": "SUGGEST_ONLY"
            }
        )


def run():
    advisor = SafeAIAdvisor()
    report = advisor.analyze_pipeline()
    print(json.dumps(asdict(report), indent=2))


if __name__ == "__main__":
    run()
