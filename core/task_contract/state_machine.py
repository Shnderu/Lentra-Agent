VALID_TRANSITIONS = {
    "pending": ["processing", "failed"],
    "processing": ["done", "failed"],
    "done": ["sent"],
    "failed": [],
    "sent": []
}


def can_transition(from_state: str, to_state: str) -> bool:
    return to_state in VALID_TRANSITIONS.get(from_state, [])
