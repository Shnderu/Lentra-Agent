class CardDetailEngine:

    def to_detail(self, state, item_id: str):
        state.mode = "DETAIL"
        state.selected_id = item_id
        return state

    def to_list(self, state):
        state.mode = "LIST"
        state.selected_id = None
        return state
