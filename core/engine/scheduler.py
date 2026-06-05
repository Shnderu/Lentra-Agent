import time
from core.db_init import init_db
from core.engine.repository import add_task


def run_scheduler():
    print(">>> SCHEDULER STARTED")

    init_db()

    while True:
        try:
            add_task("alert", {"msg": "cron tick"}, priority=10)
        except Exception as e:
            print("scheduler error:", e)

        time.sleep(10)


if __name__ == "__main__":
    run_scheduler()
