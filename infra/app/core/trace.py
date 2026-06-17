import time
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Span:
    trace_id: str
    spans: Dict[str, float] = field(default_factory=dict)

    def start(self, key: str):
        self.spans[key] = -time.time()

    def end(self, key: str):
        if key in self.spans:
            self.spans[key] += time.time()

    def report(self):
        print("\n[TRACE REPORT]")
        total = 0.0

        for k, v in self.spans.items():
            print(f"  {k}: {v*1000:.2f} ms")
            total += v

        print(f"  TOTAL: {total*1000:.2f} ms\n")
