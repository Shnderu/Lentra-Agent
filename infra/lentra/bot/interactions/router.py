from lentra.bot.state.state_store import StateStore
from lentra.bot.core.state_machine import StateMachine
from lentra.bot.services.ux_state import UXStateAdapter


class InteractionRouter:

    def __init__(self):
        self.store = StateStore()
        self.sm = StateMachine()
        self.ux = UXStateAdapter()

    async def handle(self, user_id: int, action: str, payload: str = None):

        state = self.store.load(user_id)

        if action == "next":
            state.page += 1

        elif action == "prev":
            state.page = max(0, state.page - 1)

        elif action == "open":
            state = self.sm.set_detail(state, payload)

        elif action == "back":
            state.mode = "LIST"

        self.store.save(state)

        if state.mode == "LIST":
            return self.ux.build_list_view(state)

        if state.mode == "DETAIL":
            return self.ux.build_detail_view(state)

        return "UNKNOWN STATE", None
