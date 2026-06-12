import time
import json
import redis

"""
Lentra Stability Layer v5
NLP INCIDENT REPORT GENERATOR

(упрощённый explainability слой)
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_RCA = "stream:system:rca"
STREAM_REPORTS = "stream:system:reports"


class NLPReportV5:

    def explain(self, rca):
        cause = rca.get("rca", {}).get("root_cause", "UNKNOWN")

        mapping = {
            "WORKER_BACKPRESSURE": "worker перегружен и не успевает обрабатывать поток",
            "QUEUE_OVERLOAD": "очередь задач растёт быстрее обработки",
            "STABLE": "система работает в нормальном режиме"
        }

        return mapping.get(cause, "неизвестная деградация системы")

    def run(self):
        print(">>> NLP REPORT ENGINE V5 STARTED")

        last_id = "0"

        while True:
            resp = r.xread({STREAM_RCA: last_id}, block=5000, count=10)

            if not resp:
                continue

            for _, messages in resp:
                for msg_id, msg in messages:
                    last_id = msg_id

                    explanation = self.explain(msg)

                    report = {
                        "ts": time.time(),
                        "rca": msg,
                        "human_readable": explanation,
                        "mode": "EXPLAIN_V5"
                    }

                    print(">>> REPORT:", report)

                    r.xadd(STREAM_REPORTS, report)


if __name__ == "__main__":
    NLPReportV5().run()
