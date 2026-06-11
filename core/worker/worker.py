import time

class Worker:
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        while True:
            task = self.queue.fetch_next()

            if not task:
                time.sleep(1)
                continue

            try:
                result = self.process(task)
                self.queue.mark_done(task.id, result)
            except Exception as e:
                self.queue.mark_failed(task.id, str(e))

    def process(self, task):
        return {"ok": True, "task_id": task.id}
