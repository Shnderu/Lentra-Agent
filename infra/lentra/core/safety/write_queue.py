# ============================================================
# WRITE QUEUE SYSTEM (NO DIRECT FS WRITE ALLOWED)
# ============================================================

import time
import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class WriteTask:
    path: str
    content: str
    task_type: str = "write"
    timestamp: float = time.time()
    source: str = "agent"


class WriteQueue:
    def __init__(self):
        self._queue = []

    def push(self, task: WriteTask):
        self._queue.append(task)

    def pop(self) -> Optional[WriteTask]:
        if not self._queue:
            return None
        return self._queue.pop(0)

    def dump(self):
        return [asdict(t) for t in self._queue]
