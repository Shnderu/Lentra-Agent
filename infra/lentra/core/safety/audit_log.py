# ============================================================
# WRITE AUDIT LOG (IMMUTABLE TRACE LAYER)
# ============================================================

import json
import time

AUDIT_FILE = "/opt/lentra/infra/logs/write_audit.log"


class AuditLog:

    @staticmethod
    def record(event: dict):
        event["ts"] = time.time()

        with open(AUDIT_FILE, "a") as f:
            f.write(json.dumps(event) + "\n")
