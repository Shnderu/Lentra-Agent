import time
import json
import redis
from collections import deque

"""
Lentra Stability Layer v5
ANOMALY DETECTOR (time-series lightweight model)
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"
STREAM_ANOMALIES = "stream:system:anomalies"


class AnomalyDetectorV5:

    def __init__(self):
        self.task_window = deque(maxlen=50)
        self.result_window = deque(maxlen=50)

    def load(self):
        tasks = r.xrange(STREAM_TASKS, "-", "+", count=50)
        results = r.xrange(STREAM_RESULTS, "-", "+", count=50)

        self.task_window.clear()
        self.result_window.clear()

        for _, t in tasks:
            self.task_window.append(float(t.get("ts", time.time())))

        for _, rmsg in results:
            self.result_window.append(float(rmsg.get("ts", time.time())))

    def detect_latency_spike(self):
        if len(self.task_window) < 5 or len(self.result_window) < 5:
            return False, 0

        task_rate = len(self.task_window)
        result_rate = len(self.result_window)

        lag = (task_rate - result_rate) / max(task_rate, 1)

        spike = lag > 0.4
        return spike, lag

    def run(self):
        print(">>> ANOMALY DETECTOR V5 STARTED")

        while True:
            self.load()

            spike, lag = self.detect_latency_spike()

            report = {
                "ts": time.time(),
                "anomaly": spike,
                "lag_ratio": lag,
                "severity": "HIGH" if spike else "OK",
                "mode": "PREDICTIVE_V5"
            }

            print(json.dumps(report, indent=2))

            r.xadd(STREAM_ANOMALIES, report)

            time.sleep(5)


if __name__ == "__main__":
    AnomalyDetectorV5().run()
