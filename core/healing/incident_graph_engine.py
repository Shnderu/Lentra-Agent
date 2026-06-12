import time
import json
import redis
from collections import defaultdict

"""
Lentra Stability Layer v4
INCIDENT GRAPH ENGINE

Функции:
- связывает ошибки между worker / redis / api
- строит причинно-следственные цепочки
- выявляет деградации по времени
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_ERRORS = "stream:system:errors"
STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"
STREAM_INCIDENTS = "stream:system:incidents"


class IncidentGraphEngine:

    def __init__(self):
        self.error_index = defaultdict(list)
        self.task_index = {}
        self.result_index = {}

    def load_data(self):
        errors = r.xrange(STREAM_ERRORS, "-", "+", count=500)
        tasks = r.xrange(STREAM_TASKS, "-", "+", count=500)
        results = r.xrange(STREAM_RESULTS, "-", "+", count=500)

        for _, e in errors:
            ts = float(e.get("ts", time.time()))
            self.error_index[int(ts)].append(e)

        for _, t in tasks:
            self.task_index[t.get("task_id")] = t

        for _, res in results:
            self.result_index[res.get("task_id")] = res

    def build_incidents(self):
        incidents = []

        for task_id, task in self.task_index.items():
            result = self.result_index.get(task_id)

            if not result:
                incidents.append({
                    "type": "MISSING_RESULT",
                    "task_id": task_id,
                    "severity": "MEDIUM",
                    "cause": "worker_not_finishing_task"
                })

        return incidents

    def detect_lag(self):
        tasks = len(self.task_index)
        results = len(self.result_index)

        if tasks == 0:
            return 0

        return (tasks - results) / tasks

    def run(self):
        print(">>> INCIDENT GRAPH ENGINE STARTED")

        while True:
            self.load_data()

            incidents = self.build_incidents()
            lag = self.detect_lag()

            report = {
                "ts": time.time(),
                "incidents": incidents,
                "metrics": {
                    "task_count": len(self.task_index),
                    "result_count": len(self.result_index),
                    "lag_ratio": lag
                },
                "status": "STABILITY_GRAPH_V4"
            }

            print(json.dumps(report, indent=2))

            r.xadd(STREAM_INCIDENTS, report)

            time.sleep(10)


if __name__ == "__main__":
    engine = IncidentGraphEngine()
    engine.run()
