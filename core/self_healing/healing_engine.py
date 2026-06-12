import redis
import time
import subprocess
import json

class SelfHealingEngine:
    def __init__(self, redis_host="lentra-redis"):
        self.r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

    # -----------------------------
    # STATE
    # -----------------------------
    def get_state(self):
        return {
            "tasks": int(self.r.xlen("stream:rent:tasks")),
            "results": int(self.r.xlen("stream:rent:results")),
            "trace": int(self.r.xlen("stream:rent:trace"))
        }

    # -----------------------------
    # ACTIONS (granular)
    # -----------------------------
    def restart_worker(self):
        print("[HEAL] restart worker")
        subprocess.run(["docker", "restart", "lentra-worker-stream"])

    def clear_stuck_messages(self):
        print("[HEAL] reclaim pending messages")
        # safe reclaim (not destructive)
        subprocess.run([
            "docker", "exec", "lentra-redis",
            "redis-cli", "XCLAIM",
            "stream:rent:tasks", "workers", "worker-1",
            "0", "0-0"
        ])

    def nudge_worker(self):
        print("[HEAL] nudge worker via dummy task")
        self.r.xadd("stream:rent:tasks", {
            "task_id": "heal-ping",
            "type": "system.heal",
            "payload": json.dumps({"action": "ping"}),
            "retry": "0",
            "status": "queued"
        })

    # -----------------------------
    # ROOT CAUSE DECISION ENGINE
    # -----------------------------
    def diagnose(self, state):
        if state["tasks"] > 0 and state["results"] == 0:
            if state["trace"] > 0:
                return "EXECUTION_BROKEN"
            return "WORKER_NOT_PROCESSING"

        if state["tasks"] == 0:
            return "IDLE"

        return "HEALTHY"

    # -----------------------------
    # HEALING STRATEGY MAP
    # -----------------------------
    def heal(self, cause):
        if cause == "WORKER_NOT_PROCESSING":
            self.restart_worker()

        elif cause == "EXECUTION_BROKEN":
            self.clear_stuck_messages()
            self.restart_worker()

        elif cause == "IDLE":
            self.nudge_worker()

        else:
            print("[HEAL] no action")

    # -----------------------------
    # LOOP
    # -----------------------------
    def run(self):
        print("SELF-HEALING ENGINE v2 STARTED (SMART MODE)")

        while True:
            state = self.get_state()
            cause = self.diagnose(state)

            print(f"[STATE] {state} | CAUSE={cause}")

            self.heal(cause)

            time.sleep(10)


if __name__ == "__main__":
    SelfHealingEngine().run()
