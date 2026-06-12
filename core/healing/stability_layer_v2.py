import time
import json
import traceback
import redis
import socket
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional


@dataclass
class HealthReport:
    component: str
    status: str
    error: Optional[str]
    metrics: Dict[str, Any]


class StabilityLayerV2:
    """
    SAFE AI STABILITY LAYER v2

    RULES:
    - NEVER modify runtime state
    - NEVER retry destructive actions
    - ONLY observe + diagnose + suggest
    """

    def __init__(self,
                 redis_host: str = "lentra-redis",
                 redis_port: int = 6379):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis = None

    # ---------------------------
    # CONNECTION CHECKS
    # ---------------------------

    def check_redis(self) -> HealthReport:
        try:
            r = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                decode_responses=True,
                socket_timeout=2
            )
            ping = r.ping()

            pending_tasks = 0
            try:
                pending_tasks = r.xpending("stream:rent:tasks", "workers")[0]
            except Exception:
                pass

            return HealthReport(
                component="redis",
                status="OK" if ping else "FAIL",
                error=None,
                metrics={
                    "ping": ping,
                    "pending_tasks": pending_tasks
                }
            )

        except Exception as e:
            return HealthReport(
                component="redis",
                status="FAIL",
                error=str(e),
                metrics={"trace": traceback.format_exc()}
            )

    def check_dns(self, host: str) -> HealthReport:
        try:
            ip = socket.gethostbyname(host)
            return HealthReport(
                component="dns",
                status="OK",
                error=None,
                metrics={"host": host, "ip": ip}
            )
        except Exception as e:
            return HealthReport(
                component="dns",
                status="FAIL",
                error=str(e),
                metrics={"host": host}
            )

    # ---------------------------
    # WORKER STATE CHECK
    # ---------------------------

    def analyze_stream(self) -> HealthReport:
        try:
            r = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                decode_responses=True
            )

            tasks = r.xrange("stream:rent:tasks", "-", "+")
            results = r.xrange("stream:rent:results", "-", "+")

            return HealthReport(
                component="stream",
                status="OK",
                error=None,
                metrics={
                    "tasks": len(tasks),
                    "results": len(results),
                    "delta": len(tasks) - len(results)
                }
            )

        except Exception as e:
            return HealthReport(
                component="stream",
                status="FAIL",
                error=str(e),
                metrics={}
            )

    # ---------------------------
    # ROOT CAUSE ENGINE
    # ---------------------------

    def diagnose(self) -> Dict[str, Any]:
        reports: List[HealthReport] = []

        reports.append(self.check_redis())
        reports.append(self.check_dns(self.redis_host))
        reports.append(self.analyze_stream())

        root_causes = []

        redis_report = next((r for r in reports if r.component == "redis"), None)
        stream_report = next((r for r in reports if r.component == "stream"), None)
        dns_report = next((r for r in reports if r.component == "dns"), None)

        if redis_report and redis_report.status == "FAIL":
            root_causes.append("REDIS_UNREACHABLE_OR_TIMEOUT")

        if dns_report and dns_report.status == "FAIL":
            root_causes.append("SERVICE_DISCOVERY_FAILURE")

        if stream_report and stream_report.metrics.get("delta", 0) > 0:
            root_causes.append("PIPELINE_BACKPRESSURE_OR_WORKER_LAG")

        return {
            "status": "STABILITY_REPORT_V2",
            "timestamp": time.time(),
            "reports": [asdict(r) for r in reports],
            "root_causes": root_causes,
            "severity": "HIGH" if root_causes else "LOW",
            "mode": "SUGGEST_ONLY"
        }


if __name__ == "__main__":
    layer = StabilityLayerV2()
    print(json.dumps(layer.diagnose(), indent=2))
