import time


class Metrics:

    def __init__(self):
        self.data = {}

    def start(self, name: str):
        self.data[name] = {"start": time.time()}

    def end(self, name: str):
        if name in self.data:
            self.data[name]["end"] = time.time()
            self.data[name]["latency"] = (
                self.data[name]["end"] - self.data[name]["start"]
            )

    def dump(self):
        return self.data
