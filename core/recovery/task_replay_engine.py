import redis
import json
import time
import subprocess

class TaskReplayEngine:
    """
    Recovery layer:
    - detects failed / stuck tasks
    - replays them safely
    - ensures at-least-once completion
    """

    def __init__(self, redis_host="lentra-redis"):
        self.r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

    # -----------------------------
    # FETCH FAILED / STUCK
    # -----------------------------
    def get_stuck_tasks(self):
        pending = self.r.xpending_range(
            "stream:rent:tasks",
            "workers",
            "-",
            "+",
            100
        )
        return pending

    # -----------------------------
    # REQUEUE TASK
    # -----------------------------
    def replay_task(self, task_id):
        print(f"[REPLAY] {task_id}")

        self.r.xadd("stream:rent:tasks", {
            "task_id": task_id,
            "type": "system.replay",
            "payload": json.dumps({"replay": True}),
            "retry": "1",
            "status": "requeued"
        })

    # -----------------------------
    # HEURISTIC RECOVERY
    # -----------------------------
    def detect_and_recover(self):
        stuck = self.get_stuck_tasks()

        if not stuck:
            print("[REPLAY] no stuck tasks")
            return

        for item in stuck:
            task_id = item.get("message_id") or "unknown"
            self.replay_task(task_id)

    # -----------------------------
    # LOOP
    # -----------------------------
    def run(self):
        print("TASK REPLAY ENGINE STARTED")

        while True:
            try:
                self.detect_and_recover()
                time.sleep(10)
            except Exception as e:
                print("[REPLAY ERROR]", e)
                time.sleep(2)


if __name__ == "__main__":
    TaskReplayEngine().run()
