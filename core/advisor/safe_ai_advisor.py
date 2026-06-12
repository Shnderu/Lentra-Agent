import redis
import json
import time

class SafeAIAdvisor:

    def __init__(self):
        self.r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)
        self.stream = "stream:telemetry:errors"

    def run(self):
        print("[ADVISOR] SAFE MODE ACTIVE")

        while True:
            try:
                events = self.r.xread({self.stream: "0"}, block=2000, count=1)

                if not events:
                    continue

                for stream, messages in events:
                    for msg_id, msg in messages:
                        self.analyze(msg)
                        self.r.xack(self.stream, "advisor-group", msg_id)

            except Exception as e:
                print("[ADVISOR ERROR]", e)
                time.sleep(2)

    def analyze(self, msg):
        print("[ADVISOR ANALYSIS]", msg)

        report = {
            "status": "SAFE_AI_ADVISOR",
            "root_cause": msg.get("error_type", "unknown"),
            "suggested_fixes": ["manual review required"],
            "auto_apply": False
        }

        self.r.xadd("stream:ai:advisor", report)


if __name__ == "__main__":
    SafeAIAdvisor().run()
