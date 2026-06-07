import time
import traceback

from core.engine.postgres_queue import claim_tasks, mark_done, mark_failed

WORKER_ID = "worker-1"


def handle(task):
    print(f"TASK: {task['type']} {task['payload']}")


def main():
    print("POSTGRES WORKER STARTED")

    while True:
        try:
            tasks = claim_tasks(WORKER_ID, limit=5)

            # 🔥 ЯВНЫЙ ЛОГ ПУСТОГО ЦИКЛА
            if not tasks:
                print("[WORKER] idle")
                time.sleep(2)
                continue

            for task in tasks:
                try:
                    handle(task)
                    mark_done(task["id"])
                    print(f"[WORKER] DONE {task['id']}")

                except Exception as e:
                    print(f"[WORKER] TASK ERROR {task['id']}: {e}")
                    mark_failed(task["id"], str(e))

        except Exception as e:
            print("[WORKER] LOOP ERROR")
            print(traceback.format_exc())

        time.sleep(1)


if __name__ == "__main__":
    main()
