import time
import json

class RuntimeGraph:
    def __init__(self):
        self.nodes = []

    def add(self, layer, name, payload=None):
        self.nodes.append({
            "ts": time.time(),
            "layer": layer,
            "name": name,
            "payload": payload or {}
        })

    def dump(self):
        print("\n===== RUNTIME GRAPH DUMP =====")
        for n in self.nodes:
            print(f"[{n['layer']}] {n['name']} -> {json.dumps(n['payload'], ensure_ascii=False)}")
        print("===== END GRAPH =====\n")

    def safe_call(self, label, fn, *args, **kwargs):
        self.add(label, "enter")

        try:
            result = fn(*args, **kwargs)
            self.add(label, "exit", {"ok": True})
            return result
        except Exception as e:
            self.add(label, "error", {"err": str(e)})
            return None
