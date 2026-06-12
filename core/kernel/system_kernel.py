import json

class SystemKernel:
    """
    Self-describing execution kernel.
    Stores system model as data, not code.
    """

    def __init__(self):
        self.model = {
            "layers": [
                "stream",
                "worker",
                "state_machine",
                "ledger",
                "event_store",
                "trace",
                "control_plane"
            ],
            "capabilities": [
                "execute_task",
                "recover_task",
                "replay_task",
                "optimize_dag",
                "heal_system"
            ]
        }

    # -----------------------------
    # SYSTEM SELF-ANALYSIS
    # -----------------------------
    def describe(self):
        return self.model

    # -----------------------------
    # DYNAMIC CAPABILITY CHECK
    # -----------------------------
    def has_capability(self, cap):
        return cap in self.model["capabilities"]

    # -----------------------------
    # EVOLUTION HOOK (future AI)
    # -----------------------------
    def evolve(self, new_capability):
        if new_capability not in self.model["capabilities"]:
            self.model["capabilities"].append(new_capability)
            return True
        return False
