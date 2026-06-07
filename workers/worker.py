import time
from core.engine.postgres_queue import claim_tasks


WORKER_ID = "worker-1"


def process(task):
    print(f"[WORKER] processing {task['id']} type={task['type']}")


def main():
    print("[WORKER] STARTED")

    while True:
        try:
            tasks = claim_tasks(WORKER_ID, limit=5)

            if not tasks:
                print("[WORKER] idle")
                time.sleep(2)
                continue

            for t in tasks:
                process(t)

        except Exception as e:
            print(f"[WORKER ERROR] {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
