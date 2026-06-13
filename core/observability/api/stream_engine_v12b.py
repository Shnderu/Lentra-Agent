"""
Lentra Stream Engine v12b
Live system state broadcaster
"""

import time
import json
from core.observability.system_observer_v12a import SystemObserver


class StreamEngine:

    def __init__(self):
        self.observer = SystemObserver()

    def stream(self, event_generator):

        for event in event_generator:
            snapshot = self.observer.snapshot(event)

            yield json.dumps({
                "ts": time.time(),
                "state": snapshot["system_health"],
                "risk": snapshot["prediction_v9"]["risk"]["risk_score"],
                "recurrent": snapshot["memory_v8"].get("is_recurrent", False),
                "control": snapshot["control_v10"]["decision"]["autonomy_level"]
            })

            time.sleep(1)


if __name__ == "__main__":
    def fake_events():
        while True:
            yield {
                "type": "rent.search",
                "severity": "HIGH",
                "graph_size": 7,
                "edges": 5,
                "payload": {"city": "Phu Quoc"}
            }

    stream = StreamEngine()

    for update in stream.stream(fake_events()):
        print(update)
