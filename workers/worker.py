import os
import time

import bootstrap  # BLOCKS UNTIL DB READY

from core.engine.postgres_queue import (
    claim_tasks,
    mark_done,
    mark_failed,
)

WORKER_ID = os.getenv("WORKER_ID", "worker")
BATCH_SIZE = 5

print("[WORKER START]", WORKER_ID)

while True:
    tasks = claim_tasks(WORKER_ID, BATCH_SIZE)

    if not tasks:
        print("[idle]")
        time.sleep(2)
        continue

    for t in tasks:
        try:
            print("[TASK]", t["id"])
            mark_done(t["id"], WORKER_ID)
        except Exception as e:
            mark_failed(t["id"], WORKER_ID, str(e))
