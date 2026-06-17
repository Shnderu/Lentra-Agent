# ============================================================
# WRITE WORKER (ONLY PLACE WHERE FS WRITE IS ALLOWED)
# ============================================================

import os
from lentra.core.safety.write_queue import WriteQueue
from lentra.core.safety.audit_log import AuditLog


class WriteWorker:
    def __init__(self, queue: WriteQueue):
        self.queue = queue

    def run_once(self):
        task = self.queue.pop()

        if not task:
            return

        # audit BEFORE write
        AuditLog.record({
            "action": "write",
            "path": task.path,
            "source": task.source
        })

        os.makedirs(os.path.dirname(task.path), exist_ok=True)

        with open(task.path, "w") as f:
            f.write(task.content)
