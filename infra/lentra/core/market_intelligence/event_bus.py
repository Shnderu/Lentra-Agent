class EventBus:
    """
    HOTFIX: временный in-process event bus
    """

    def __init__(self, event_log=None):
        self.event_log = event_log

    def subscribe(self, event_type, handler):
        pass

    def publish(self, event):
        # safe no-op (synchronous compatibility)
        if self.event_log:
            self.event_log.append(event)
        return True
