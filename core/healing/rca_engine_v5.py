import time
import json
import redis

"""
Lentra Stability Layer v5
ROOT CAUSE ANALYSIS ENGINE (RCA)
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_ANOMALIES = "stream:system:anomalies"
STREAM_RCA = "stream:system:rca"


class RCAEngineV5:

    def classify_root_cause(self, anomaly):
        lag = anomaly.get("lag_ratio", 0)

        if lag > 0.7:
            return {
                "root_cause": "WORKER_BACKPRESSURE",
                "confidence": 0.9
            }

        if lag > 0.4:
            return {
                "root_cause": "QUEUE_OVERLOAD",
                "confidence": 0.75
            }

        return {
            "root_cause": "STABLE",
            "confidence": 0.5
        }

    def run(self):
        print(">>> RCA ENGINE V5 STARTED")

        last_id = "0"

        while True:
            resp = r.xread({STREAM_ANOMALIES: last_id}, block=5000, count=10)

            if not resp:
                continue

            for _, messages in resp:
                for msg_id, msg in messages:
                    last_id = msg_id

                    rca = self.classify_root_cause(msg)

                    report = {
                        "ts": time.time(),
                        "anomaly": msg,
                        "rca": rca,
                        "mode": "RCA_V5"
                    }

                    print(">>> RCA:", report)

                    r.xadd(STREAM_RCA, report)


if __name__ == "__main__":
    RCAEngineV5().run()
