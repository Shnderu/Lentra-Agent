import json
from lentra.runtime.arch_lock.sealed_graph import SealedGraph


class SealEngine:
    """
    Enforces immutable architecture graph at runtime.
    """

    SNAPSHOT_FILE = "/opt/lentra/infra/lentra/runtime/arch_lock/SEAL.json"

    def build_snapshot(self):
        sg = SealedGraph()
        graph = sg.build("/opt/lentra/infra/lentra")

        return {
            "graph": graph,
            "fingerprint": sg.fingerprint(graph)
        }

    def save_snapshot(self):
        snapshot = self.build_snapshot()

        with open(self.SNAPSHOT_FILE, "w") as f:
            json.dump(snapshot, f, indent=2)

        print("[SEAL] snapshot saved:", snapshot["fingerprint"])

    def validate(self):
        sg = SealedGraph()
        current = self.build_snapshot()

        try:
            with open(self.SNAPSHOT_FILE, "r") as f:
                previous = json.load(f)
        except Exception:
            raise RuntimeError("[SEAL] missing baseline snapshot")

        if current["fingerprint"] != previous["fingerprint"]:
            raise RuntimeError("[SEAL] ARCH DRIFT DETECTED")

        print("[SEAL] OK - architecture sealed")
