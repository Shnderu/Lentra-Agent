import time
import random


def retry(fn, attempts=3, base_delay=0.5):
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:
            if i == attempts - 1:
                raise e
            delay = base_delay * (2 ** i) + random.uniform(0, 0.2)
            time.sleep(delay)
