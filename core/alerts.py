class AlertEngine:
    def __init__(self):
        self.subscriptions = {}

    def subscribe(self, user_id: int, route: str):
        self.subscriptions[user_id] = route

    def check_alert(self, user_id: int, data: dict):
        route = self.subscriptions.get(user_id)
        if not route:
            return None

        if route in data.get("route", ""):
            return f"🔥 Alert: price movement detected on {route}"

        return None
