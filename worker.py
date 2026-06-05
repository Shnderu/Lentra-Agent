import time
from core.engine.redis_queue import pop_task

print("WORKER STARTED")


def process_task(task: str):
    """
    Здесь будет твоя бизнес-логика обработки задач.
    Сейчас — просто лог.
    """
    print(f"PROCESS TASK: {task}")

    # TODO: добавить обработку (API, поиск, travel engine и т.д.)
    # например:
    # travel_engine.handle(task)


def main():
    while True:
        try:
            task = pop_task()

            if task:
                print(f"DEBUG TASK: {task}")
                process_task(task)
            else:
                # важно: не грузим CPU
                time.sleep(1)

        except Exception as e:
            print(f"WORKER ERROR: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
