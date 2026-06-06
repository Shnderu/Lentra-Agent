from core.engine.postgres_queue import push_task


def enqueue_flight(user_id: int, origin: str, destination: str):
    """
    Пушит задачу в очередь Postgres
    """
    return push_task(
        task_type="flight_search",
        payload={
            "user_id": user_id,
            "origin": origin,
            "destination": destination
        },
        priority=5
    )
