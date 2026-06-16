class CallbackParser:

    @staticmethod
    def parse(data: str):

        parts = data.split(":")

        if parts[0] == "search":
            return {
                "type": "search_page",
                "search_id": parts[1],
                "page": int(parts[3])
            }

        if parts[0] == "item":
            return {
                "type": "item_open",
                "item_id": parts[1]
            }

        if parts[0] == "back":
            return {
                "type": "back_to_list",
                "search_id": parts[2]
            }

        if parts[0] == "filter":
            return {
                "type": "filter_open"
            }

        return {"type": "unknown"}
