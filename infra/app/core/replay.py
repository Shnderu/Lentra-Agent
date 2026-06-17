import time


class ReplayEngine:
    def __init__(self, bus, dlq):
        self.bus = bus
        self.dlq = dlq

    def replay_all(self, span, graph):
        if not self.dlq.items:
            print("[REPLAY] empty DLQ")
            return

        print(f"\n[REPLAY] start items={len(self.dlq.items)}")

        items = list(self.dlq.items)
        self.dlq.items.clear()

        for item in items:
            print(f"[REPLAY EVENT] {item}")

            event = type("Event", (), {
                "type": item["event"],
                "payload": item["payload"],
                "trace_id": span.trace_id
            })()

            time.sleep(0.05)

            self.bus.publish(event, span, graph)
