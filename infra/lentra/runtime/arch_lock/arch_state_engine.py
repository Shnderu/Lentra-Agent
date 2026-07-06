import json
import hashlib
import time


class ArchStateEngine:
    """
    Stores versioned architecture snapshots.
    """

    STATE_FILE = "/opt/lentra/infra/lentra/runtime/arch_lock/ARCH_STATE.json"

    def load(self):
        try:
            with open(self.STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {"versions": []}

    def save(self, state: dict):
        with open(self.STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

    def create_version(self, snapshot: dict):
        state = self.load()

        version = {
            "ts": time.time(),
            "fingerprint": snapshot.get("fingerprint"),
            "graph_hash": hashlib.sha256(
                json.dumps(snapshot.get("graph", {}), sort_keys=True).encode()
            ).hexdigest()
        }

        state["versions"].append(version)
        self.save(state)

        return version
