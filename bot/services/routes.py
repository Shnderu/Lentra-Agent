# /opt/flyrum/bot/services/routes.py

import json
from core.engine.redis_queue import push_task as redis_push_task


def add_route(user_id: int, origin: str, destination: str):
    """
    Создание задачи поиска маршрута / перелета
    """

    task_payload = {
        "user_id": user_id,
        "origin": origin,
        "destination": destination,
    }

    # ВАЖНО: исправление сигнатуры push_task
    # (убраны task_type и keyword-аргументы)
    task_id = redis_push_task(
        json.dumps({
            "type": "flight_search",
            "payload": task_payload,
            "priority": 5
        })
    )

    return task_id
