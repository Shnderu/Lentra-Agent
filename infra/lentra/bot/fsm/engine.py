from lentra.bot.fsm.transitions import ALLOWED_TRANSITIONS


class InvalidTransition(Exception):
    pass


class FSMEngine:

    def transition(self, state, next_state: str):

        current = state.current_state

        allowed = ALLOWED_TRANSITIONS.get(
            current,
            set()
        )

        if next_state not in allowed:
            raise InvalidTransition(
                f"{current} -> {next_state}"
            )

        state.previous_state = current

        state.history.append(current)

        state.current_state = next_state

        return state

    def back(self, state):

        if not state.history:
            return state

        state.current_state = state.history.pop()

        return state
