from core.alerts.engine import AlertEngine

alert_engine = AlertEngine()


async def watch_worker(task):

    payload = task["payload"]

    result = alert_engine.process_watch(payload)

    print("[ALERT RESULT]", result)

    return result
