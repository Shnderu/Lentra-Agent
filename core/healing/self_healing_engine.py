import redis
import json
import time

class SelfHealingEngine:
    """
    SAFE MODE:
    - only reacts to explicit diagnostics signals
    - NEVER auto-executes fixes
    """

    def __init__(self):
        self.r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)
        self.channel = "stream:telemetry:errors"

    def listen(self):
        print("[HEALING] engine started (SAFE MODE)")

        while True:
            try:
                events = self.r.xread({self.channel: "0"}, block=2000, count=1)

                if not events:
                    continue

                for stream, messages in events:
                    for msg_id, msg in messages:
                        self.handle(msg)
                        self.r.xack(self.channel, "healing-group", msg_id)

            except Exception as e:
                print("[HEALING ERROR]", e)
                time.sleep(2)

    def handle(self, msg):
        print("[HEALING EVENT]", msg)

        # IMPORTANT: NO AUTO FIX HERE
        decision = {
            "action": "SUGGEST_ONLY",
            "root_cause": msg.get("error_type", "unknown"),
            "confidence": 0.0
        }

        self.r.xadd("stream:healing:decisions", decision)


if __name__ == "__main__":
    SelfHealingEngine().listen()
