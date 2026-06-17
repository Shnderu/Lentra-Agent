from concurrent.futures import ThreadPoolExecutor
import queue


class TaskExecutor:
    def __init__(self, max_workers=4, max_queue=20):
        self.pool = ThreadPoolExecutor(max_workers=max_workers)
        self.queue = queue.Queue(maxsize=max_queue)
        self.dlq = []

    def submit(self, fn, *args, **kwargs):
        if self.queue.full():
            print("[BACKPRESSURE] queue full -> DLQ")
            self.dlq.append((fn, args, kwargs))
            return None

        self.queue.put(True)

        def wrapper():
            try:
                return fn(*args, **kwargs)
            finally:
                self.queue.get()

        return self.pool.submit(wrapper)
