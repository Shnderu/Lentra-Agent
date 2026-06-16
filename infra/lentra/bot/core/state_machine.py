from lentra.bot.state.session import SessionState


class StateMachine:

    def set_list(self, state: SessionState, items: list, query: str, search_id: str):

        state.mode = "LIST"
        state.query = query
        state.search_id = search_id
        state.page = 0

        # ❗ ONLY IDS (state slimming)
        state.result_ids = [i.id for i in items]

        state.selected_id = None

        return state

    def set_detail(self, state: SessionState, item_id: str):

        state.mode = "DETAIL"
        state.selected_id = item_id

        return state
