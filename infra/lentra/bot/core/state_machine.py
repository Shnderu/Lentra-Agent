from lentra.bot.state.session import SessionState


class StateMachine:

    def set_list(self, state: SessionState, results: list, query: str, search_id: str):

        state.mode = "LIST"
        state.query = query
        state.search_id = search_id
        state.page = 0

        state.results = [
            {
                "id": r.id if hasattr(r, "id") else r.get("id"),
                "title": r.title if hasattr(r, "title") else r.get("title"),
                "city": r.city if hasattr(r, "city") else r.get("city"),
                "district": r.district if hasattr(r, "district") else r.get("district"),
                "price_vnd_mln": r.price_vnd_mln if hasattr(r, "price_vnd_mln") else r.get("price_vnd_mln"),
                "score": r.score if hasattr(r, "score") else r.get("score"),
                "pool": getattr(r, "pool", r.get("pool", False)),
                "sea_view": getattr(r, "sea_view", r.get("sea_view", False)),
            }
            for r in results
        ]

        state.selected_id = None
        return state

    def set_detail(self, state: SessionState, item_id: str):
        state.mode = "DETAIL"
        state.selected_id = item_id
        return state

    def next_page(self, state: SessionState):
        state.page += 1
        return state

    def prev_page(self, state: SessionState):
        state.page = max(0, state.page - 1)
        return state
