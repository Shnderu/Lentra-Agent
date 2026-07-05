class EventBusSafe:

    def publish(self, event):
        # NO SIDE EFFECT OUTPUT ALLOWED
        return event

    def emit(self, event):
        return event
