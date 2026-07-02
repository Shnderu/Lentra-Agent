import time
import uuid


class TraceCollector:
    def __init__(self):
        self.traces = {}

    def start(self, payload: dict):
        trace_id = str(uuid.uuid4())

        self.traces[trace_id] = {
            "start": time.time(),
            "payload": payload,
            "events": []
        }

        return trace_id

    def event(self, trace_id: str, event: str):
        if trace_id in self.traces:
            self.traces[trace_id]["events"].append({
                "t": time.time(),
                "event": event
            })

    def finish(self, trace_id: str, result: dict):
        if trace_id in self.traces:
            self.traces[trace_id]["end"] = time.time()
            self.traces[trace_id]["result"] = result

    def get(self, trace_id: str):
        return self.traces.get(trace_id, {})
