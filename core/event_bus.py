_subscribers = {}


def subscribe(topic: str, callback):
    if topic not in _subscribers:
        _subscribers[topic] = []
    _subscribers[topic].append(callback)


def publish(topic: str, event):
    if topic not in _subscribers:
        return

    for cb in _subscribers[topic]:
        try:
            cb(event)
        except Exception as e:
            print("[EVENT BUS ERROR]", e)
