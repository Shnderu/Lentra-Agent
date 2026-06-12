from core.kernel.system_kernel import SystemKernel

class ControlPlane:
    def __init__(self):
        self.kernel = SystemKernel()

    def decide(self, state, trace, ledger):
        model = self.kernel.describe()

        tasks = state.get("tasks", 0)
        results = state.get("results", 0)
        trace_size = state.get("trace", 0)

        capabilities = model["capabilities"]

        # -----------------------------
        # SYSTEM LOGIC IS NOW MODEL-AWARE
        # -----------------------------
        if "heal_system" in capabilities and tasks > 0 and results == 0:
            return {
                "mode": "SELF_HEALING_KERNEL",
                "plan": [
                    {"action": "restart_worker", "priority": 1},
                    {"action": "replay_tasks", "priority": 2}
                ]
            }

        if tasks == 0:
            return {
                "mode": "DORMANT",
                "plan": [
                    {"action": "scale_down", "priority": 1}
                ]
            }

        return {
            "mode": "STABLE",
            "plan": [
                {"action": "no_op", "priority": 1}
            ]
        }
