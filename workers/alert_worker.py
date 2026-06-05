import time
from core.task_queue import fetch_task, complete_task, fail_task


def handle(task):
    print(
        f"[WORKER] task={task['id']} "
        f"type={task['type']} "
        f"payload={task['payload']}"
    )


def main():
    print(">>> WORKER STARTED")

    while True:
        task = fetch_task()

        if not task:
            print("[WORKER] idle tick")
            time.sleep(2)
            continue

        try:
            handle(task)
            complete_task(task["id"])

            print(f"[WORKER] DONE {task['id']}")

        except Exception as e:
            print(f"[WORKER] ERROR {task['id']} -> {e}")
            fail_task(task)

        time.sleep(1)


if __name__ == "__main__":
    main()
