

# simple in-memory learning store (v1)

USER_FEEDBACK = {}


def record_feedback(query, listing_id, action):

    key = f"{query}:{listing_id}"

    if key not in USER_FEEDBACK:
        USER_FEEDBACK[key] = {
            "click": 0,
            "ignore": 0,
            "save": 0
        }

    USER_FEEDBACK[key][action] += 1

    return USER_FEEDBACK[key]


def get_feedback_score(query, listing_id):

    key = f"{query}:{listing_id}"

    if key not in USER_FEEDBACK:
        return 0.0

    f = USER_FEEDBACK[key]

    return (
        f["click"] * 0.2 +
        f["save"] * 0.5 -
        f["ignore"] * 0.3
    )
