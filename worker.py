import time
from core.engine.postgres_queue import claim_tasks, mark_done, mark_failed

WORKER_ID = "worker-1"


def handle(task):
    print(f"TASK: {task['type']} {task['payload']}")


def main():
    print("POSTGRES WORKER STARTED")

    while True:
        tasks = claim_tasks(WORKER_ID, limit=5)

        if not tasks:
            print("CLAIMED TASKS: []")
            time.sleep(2)
            continue

        print(f"CLAIMED TASKS: {tasks}")

        for task in tasks:
            try:
                handle(task)
                mark_done(task["id"])
            except Exception as e:
                mark_failed(task["id"], str(e))

        time.sleep(1)


if __name__ == "__main__":
    main()
