from core.engine.redis_queue import pop_task
import time


def main():
    print("WORKER STARTED")

    while True:
        task = pop_task()

        print("DEBUG TASK:", task)

        time.sleep(2)


if __name__ == "__main__":
    main()
