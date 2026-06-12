import traceback
import time

"""
Lentra Diagnostics v6-lite
Error Schema Normalizer
"""


def normalize_error(e: Exception, context: str = None):
    return {
        "ts": time.time(),
        "error_type": type(e).__name__,
        "message": str(e),
        "context": context,
        "trace": traceback.format_exc()
    }
