import time


def track(event_type: str, payload: dict):
    print(f"[OBS] {event_type}", payload)
