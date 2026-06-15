from lentra.bot.state.session import SessionState

from lentra.bot.fsm.engine import FSMEngine

from lentra.bot.fsm.states import (
    LIST,
    DETAIL
)


class StateMachine:

    def __init__(self):
        self.fsm = FSMEngine()

    def set_list(
        self,
        state: SessionState,
        results: list,
        query: str,
        search_id: str
    ):

        if state.current_state != "IDLE":
            state = self.fsm.transition(
                state,
                LIST
            )
        else:
            state.current_state = LIST

        state.query = query

        state.search_id = search_id

        state.page = 0

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

        state.mode = LIST

        return state

    def set_detail(
        self,
        state: SessionState,
        item_id: str
    ):

        state = self.fsm.transition(
            state,
            DETAIL
        )

        state.selected_id = item_id

        state.mode = DETAIL

        return state

    def back(self, state: SessionState):

        state = self.fsm.back(state)

        state.mode = state.current_state

        return state
