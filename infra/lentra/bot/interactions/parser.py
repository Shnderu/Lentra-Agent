class CallbackParser:

    @staticmethod
    def parse(data: str):

        if ":" not in data:
            return data, None

        action, payload = data.split(":", 1)

        return action, payload
