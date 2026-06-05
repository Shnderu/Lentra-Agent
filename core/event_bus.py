import asyncio

_subscribers = {}


def subscribe(topic: str, callback):
    if topic not in _subscribers:
        _subscribers[topic] = []
    _subscribers[topic].append(callback)


async def _safe_call(cb, event):
    try:
        if asyncio.iscoroutinefunction(cb):
            await cb(event)
        else:
            cb(event)
    except Exception as e:
        print("[EVENT BUS ERROR]", e)


def publish(topic: str, event):
    if topic not in _subscribers:
        return

    loop = asyncio.get_event_loop()

    for cb in _subscribers[topic]:
        loop.create_task(_safe_call(cb, event))
