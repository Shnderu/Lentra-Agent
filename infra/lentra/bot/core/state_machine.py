from lentra.bot.state.session import SessionState


class StateMachine:

    def set_list(self, state: SessionState, results: list, query: str, search_id: str):

        state.mode = "LIST"
        state.query = query
        state.search_id = search_id
        state.page = 0

        # IMPORTANT: results must contain stable id
        state.results = [
            {
                "id": r.id,
                "title": r.title,
                "city": r.city,
                "district": r.district,
                "price_vnd_mln": r.price_vnd_mln,
                "score": r.score
            }
            for r in results
        ]

        state.selected_id = None
        return state

    def set_detail(self, state: SessionState, item_id: str):
        state.mode = "DETAIL"
        state.selected_id = item_id
        return state
