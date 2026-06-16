from lentra.bot.state.state_store import SessionState


class UXEngine:

    def to_list(self, state: SessionState, results, search_id: str):

        state.mode = "LIST"
        state.search_id = search_id
        state.page = 0
        state.selected_id = None

        return state

    def to_page(self, state: SessionState, page: int):

        state.page = max(0, page)
        return state

    def to_detail(self, state: SessionState, item_id: str):

        state.mode = "DETAIL"
        state.selected_id = item_id
        return state

    def back_to_list(self, state: SessionState):

        state.mode = "LIST"
        state.selected_id = None

        return state
