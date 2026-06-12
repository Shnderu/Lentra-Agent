import time
import threading


class GlobalScheduler:
    """
    Simple global tick scheduler (future cron + SLA + retry coordination layer).
    """

    def __init__(self, tick_interval=5):
        self.tick_interval = tick_interval
        self.jobs = []

    def add_job(self, fn):
        self.jobs.append(fn)

    def start(self):
        def loop():
            while True:
                for job in self.jobs:
                    try:
                        job()
                    except Exception:
                        pass
                time.sleep(self.tick_interval)

        t = threading.Thread(target=loop, daemon=True)
        t.start()
        return t
