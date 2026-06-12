"""
Lentra Policy Engine v10
Decision Safety Guardrails
"""


class PolicyEngine:

    def validate(self, actions: list):
        approved = []
        rejected = []

        for action in actions:

            if action["action"] == "RESTART_WORKER_POOL":
                rejected.append({
                    "action": action,
                    "reason": "requires manual approval"
                })
                continue

            if action["action"] == "SCALE_RESOURCES":
                approved.append(action)
                continue

            if action["action"] == "CHECK_QUEUE_BACKPRESSURE":
                approved.append(action)

        return {
            "approved": approved,
            "rejected": rejected,
            "policy_mode": "SAFE_GUARD_ACTIVE"
        }


if __name__ == "__main__":
    print("Policy engine ready")
