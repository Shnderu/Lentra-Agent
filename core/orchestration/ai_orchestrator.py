import redis
import time
import subprocess
from core.control_plane.control_plane import ControlPlane

class AIOrchestrationBrain:
    def __init__(self, redis_host="lentra-redis"):
        self.r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        self.control = ControlPlane()

    def state(self):
        return {
            "tasks": int(self.r.xlen("stream:rent:tasks")),
            "results": int(self.r.xlen("stream:rent:results")),
            "trace": int(self.r.xlen("stream:rent:trace"))
        }

    def trace(self, limit=50):
        data = self.r.xrevrange("stream:rent:trace", count=limit)
        return [f"{d}" for _, d in data]

    def ledger(self):
        return {}

    # -----------------------------
    # EXECUTION ENGINE
    # -----------------------------
    def execute_plan(self, plan):
        # sort by priority (lower = higher priority)
        plan = sorted(plan, key=lambda x: x.get("priority", 999))

        for step in plan:
            action = step["action"]

            print(f"[EXEC] {action}")

            if action == "restart_worker":
                subprocess.run(["docker", "restart", "lentra-worker-stream"])

            elif action == "replay_tasks":
                print("[ACTION] trigger replay engine hook")

            elif action == "inspect_trace":
                print("[ACTION] trace inspection")

            elif action == "check_pipeline":
                print("[ACTION] pipeline validation")

            elif action == "scale_down":
                print("[ACTION] scaling workers down (stub)")

            elif action == "no_op":
                pass

    # -----------------------------
    # LOOP
    # -----------------------------
    def run(self):
        print("AI CONTROL PLANE v2 STARTED")

        while True:
            state = self.state()
            trace = self.trace()
            ledger = self.ledger()

            decision = self.control.decide(state, trace, ledger)

            print("[DECISION]", decision["mode"], "conf=", decision["confidence"])

            self.execute_plan(decision["plan"])

            time.sleep(10)


if __name__ == "__main__":
    AIOrchestrationBrain().run()
