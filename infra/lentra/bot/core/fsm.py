from lentra.bot.core.state_machine import StateMachine


class FSMEngine:
    """
    Adapter layer over StateMachine
    Provides high-level UI state transitions expected by pipeline
    """

    def __init__(self):
        self.sm = StateMachine()

    def handle(self, state, event: dict):

        t = event["type"]

        if t == "search_completed":
            return self.sm.on_search_completed(
                state,
                event["payload"]["results"],
                event["payload"]["query"],
                event["payload"]["search_id"]
            )

        if t == "item_selected":
            return self.sm.on_item_selected(
                state,
                event["payload"]["item_id"]
            )

        if t == "back":
            return self.sm.on_back(state)

        if t == "page":
            return self.sm.on_page(state, event["payload"]["page"])

        return state

    # =========================
    # COMPAT LAYER (FIX CRASH)
    # =========================

    def set_list(self, state, items, query, search_id):
        event = {
            "type": "search_completed",
            "payload": {
                "results": items,
                "query": query,
                "search_id": search_id
            }
        }
        return self.handle(state, event)

    def set_detail(self, state, item_id):
        event = {
            "type": "item_selected",
            "payload": {
                "item_id": item_id
            }
        }
        return self.handle(state, event)

    def set_page(self, state, page: int):
        event = {
            "type": "page",
            "payload": {
                "page": page
            }
        }
        return self.handle(state, event)
