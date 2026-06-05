import time
import logging

from core.engine.redis_queue import pop_task, push_result

logging.basicConfig(level=logging.INFO)


def process(task: dict):
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


def safe_extract(task: dict):
    """
    Жесткая защита от битых задач
    """
    if not isinstance(task, dict):
        return None, None

    task_id = task.get("id")
    payload = task.get("payload")

    if not task_id or not isinstance(payload, dict):
        return None, None

    user_id = payload.get("user_id")

    if not user_id:
        return None, None

    return task_id, user_id


def main():
    print("WORKER STARTED")

    while True:
        try:
            task = pop_task()

            if not task:
                time.sleep(1)
                continue

            task_id, user_id = safe_extract(task)

            if not task_id or not user_id:
                logging.warning(f"SKIP BAD TASK: {task}")
                continue

            result_data = process(task)

            push_result({
                "task_id": task_id,
                "user_id": user_id,
                "data": result_data
            })

        except Exception as e:
            logging.error(f"WORKER CRASH-PROTECTED ERROR: {e}")

        time.sleep(1)


if __name__ == "__main__":
    main()
