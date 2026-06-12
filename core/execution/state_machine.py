class ExecutionStateMachine:
    """
    Deterministic execution model.
    Defines allowed transitions.
    """

    VALID_TRANSITIONS = {
        "created": ["queued"],
        "queued": ["processing", "failed"],
        "processing": ["done", "failed"],
        "failed": ["queued"],
        "done": []
    }

    def can_transition(self, from_state, to_state):
        return to_state in self.VALID_TRANSITIONS.get(from_state, [])

    def validate(self, from_state, to_state):
        if not self.can_transition(from_state, to_state):
            raise Exception(f"INVALID_TRANSITION {from_state} -> {to_state}")

    def next(self, current_state, event):
        if current_state == "created" and event == "enqueue":
            return "queued"

        if current_state == "queued" and event == "start":
            return "processing"

        if current_state == "processing" and event == "success":
            return "done"

        if current_state == "processing" and event == "error":
            return "failed"

        return current_state
