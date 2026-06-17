class DeadLetterQueue:
    def __init__(self):
        self.items = []

    def push(self, event, reason):
        self.items.append({
            "event": event.type,
            "payload": event.payload,
            "reason": reason
        })

    def dump(self):
        print("\n[DLQ]")
        for i in self.items:
            print(i)
