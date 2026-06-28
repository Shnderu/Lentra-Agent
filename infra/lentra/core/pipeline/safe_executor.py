import time
import traceback
from typing import Any, Callable


class SafeExecutor:

    def __init__(self, max_retries: int = 3, base_delay: float = 0.5):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def run(self, fn: Callable, *args, **kwargs) -> Any:
        last_error = None

        for attempt in range(self.max_retries):
            try:
                return fn(*args, **kwargs)

            except Exception as e:
                last_error = e

                print(f"[RETRY] attempt={attempt + 1} error={str(e)}", flush=True)
                traceback.print_exc()

                time.sleep(self.base_delay * (2 ** attempt))

        raise last_error
