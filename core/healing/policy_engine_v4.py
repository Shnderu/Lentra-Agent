import time
import json
import redis

"""
Lentra Stability Layer v4
POLICY ENGINE (controlled decisions only)
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_INCIDENTS = "stream:system:incidents"
STREAM_POLICIES = "stream:system:policies"


class PolicyEngineV4:

    def classify(self, incident):
        if incident["type"] == "MISSING_RESULT":
            return {
                "action": "RETRY_TASK",
                "priority": "HIGH",
                "safe": True
            }

        return {
            "action": "NOOP",
            "priority": "LOW",
            "safe": True
        }

    def run(self):
        print(">>> POLICY ENGINE V4 STARTED")

        last_id = "0"

        while True:
            resp = r.xread({STREAM_INCIDENTS: last_id}, block=5000, count=10)

            if not resp:
                continue

            for _, messages in resp:
                for msg_id, msg in messages:
                    last_id = msg_id

                    incidents = msg.get("incidents", [])

                    for inc in incidents:
                        policy = self.classify(inc)

                        payload = {
                            "incident": inc,
                            "policy": policy,
                            "ts": time.time(),
                            "mode": "SAFE_POLICY_V4"
                        }

                        print(">>> POLICY:", payload)

                        r.xadd(STREAM_POLICIES, payload)


if __name__ == "__main__":
    PolicyEngineV4().run()
