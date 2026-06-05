import time
import json
import logging

from core.engine.redis_queue import pop_task, push_result

logging.basicConfig(level=logging.INFO)

def process(task: dict):
    # временная mock логика (позже Kiwi API)
    return {
        "results": [
            {
                "from": "MOW",
                "to": "DXB",
                "price": 120,
                "duration": 5,
                "airline": "FlyRum Mock"
            }
        ]
    }


def main():
    print("WORKER STARTED")

    while True:
        raw = pop_task()

        if raw:
            try:
                task = json.loads(raw)

                user_id = task["payload"]["user_id"]
                task_id = task["id"]

                result_data = process(task)

                push_result(json.dumps({
                    "task_id": task_id,
                    "user_id": user_id,
                    "data": result_data
                }))

            except Exception as e:
                logging.error(f"WORKER ERROR: {e}")

        time.sleep(1)


if __name__ == "__main__":
    main()
