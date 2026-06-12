import time
import json
import redis

"""
Lentra Stability Layer v5
REGRESSION FINGERPRINT ENGINE

Сравнивает поведение системы во времени
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"
STREAM_FINGERPRINT = "stream:system:fingerprint"


class FingerprintEngineV5:

    def run(self):
        print(">>> REGRESSION FINGERPRINT V5 STARTED")

        last_task_count = 0
        last_result_count = 0

        while True:
            tasks = len(r.xrange(STREAM_TASKS, "-", "+"))
            results = len(r.xrange(STREAM_RESULTS, "-", "+"))

            delta_tasks = tasks - last_task_count
            delta_results = results - last_result_count

            fingerprint = {
                "ts": time.time(),
                "tasks_delta": delta_tasks,
                "results_delta": delta_results,
                "loss_ratio": (delta_tasks - delta_results) / max(delta_tasks, 1) if delta_tasks else 0,
                "mode": "FINGERPRINT_V5"
            }

            print(json.dumps(fingerprint, indent=2))

            r.xadd(STREAM_FINGERPRINT, fingerprint)

            last_task_count = tasks
            last_result_count = results

            time.sleep(10)


if __name__ == "__main__":
    FingerprintEngineV5().run()
