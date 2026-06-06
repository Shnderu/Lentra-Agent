from core.engine.postgres_queue import claim_tasks, mark_done, mark_failed

WORKER_ID = "worker-1"


def main():
    print("POSTGRES WORKER STARTED")

    while True:
        try:
            tasks = claim_tasks(WORKER_ID, limit=5)

            if not tasks:
                continue

            for task in tasks:
                # ⚠️ FIX: tuple unpacking (не dict!)

                task_id = task[0]
                task_type = task[1]
                payload = task[2]

                print("TASK:", task_type)

                try:
                    mark_done(task_id)

                except Exception as e:
                    mark_failed(task_id, str(e))

        except Exception as e:
            print("WORKER LOOP ERROR:", str(e))


if __name__ == "__main__":
    main()
