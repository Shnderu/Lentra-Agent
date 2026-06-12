import time
import traceback
import redis
import socket
from dataclasses import dataclass, asdict
from typing import Dict, Any, List


# -----------------------------
# CONFIG
# -----------------------------
REDIS_HOST = "lentra-redis"
REDIS_PORT = 6379

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"


# -----------------------------
# STATE MODEL
# -----------------------------
@dataclass
class ErrorEvent:
    source: str
    error_type: str
    message: str
    trace: str
    ts: float


@dataclass
class SystemHealth:
    status: str
    root_cause: str
    severity: str
    errors: List[ErrorEvent]


# -----------------------------
# CORE ENGINE
# -----------------------------
class StabilityEngine:

    def __init__(self):
        self.r = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True,
            socket_timeout=5
        )
        self.errors: List[ErrorEvent] = []

    # -------------------------
    # HEALTH CHECKS
    # -------------------------
    def check_redis(self) -> bool:
        try:
            return self.r.ping()
        except Exception as e:
            self._record("redis", e)
            return False

    def check_streams(self) -> Dict[str, Any]:
        try:
            tasks = self.r.xlen(STREAM_TASKS)
            results = self.r.xlen(STREAM_RESULTS)
            return {"tasks": tasks, "results": results}
        except Exception as e:
            self._record("stream", e)
            return {}

    # -------------------------
    # ERROR HANDLING
    # -------------------------
    def _record(self, source: str, error: Exception):
        self.errors.append(
            ErrorEvent(
                source=source,
                error_type=type(error).__name__,
                message=str(error),
                trace=traceback.format_exc(),
                ts=time.time()
            )
        )

    # -------------------------
    # ROOT CAUSE ENGINE
    # -------------------------
    def analyze(self) -> SystemHealth:

        if not self.errors:
            return SystemHealth(
                status="HEALTHY",
                root_cause="NO_FAILURES",
                severity="NONE",
                errors=[]
            )

        # classify
        redis_fail = any(e.source == "redis" for e in self.errors)
        stream_fail = any(e.source == "stream" for e in self.errors)

        if redis_fail:
            root = "REDIS_UNREACHABLE_OR_TIMEOUT"
            severity = "HIGH"

        elif stream_fail:
            root = "STREAM_LAYER_BROKEN"
            severity = "HIGH"

        else:
            root = "UNKNOWN_FAILURE"
            severity = "MEDIUM"

        return SystemHealth(
            status="DEGRADED",
            root_cause=root,
            severity=severity,
            errors=self.errors[-10:]
        )

    # -------------------------
    # MAIN RUN
    # -------------------------
    def run_once(self):
        self.errors.clear()

        redis_ok = self.check_redis()
        streams = self.check_streams()

        health = self.analyze()

        print({
            "redis_ok": redis_ok,
            "streams": streams,
            "health": asdict(health)
        })

        return health


if __name__ == "__main__":
    engine = StabilityEngine()
    while True:
        try:
            engine.run_once()
        except Exception as e:
            print("[STABILITY ENGINE CRASH]", e)

        time.sleep(5)
