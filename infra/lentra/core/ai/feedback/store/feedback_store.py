

FEEDBACK_LOG = []


def log_feedback(user_id: str, listing_id: str, action: str, score: float = 1.0):

    """
    action:
      - click
      - ignore
      - save
      - reject
    """

    FEEDBACK_LOG.append({
        "user_id": user_id,
        "listing_id": listing_id,
        "action": action,
        "score": score
    })


def get_feedback():
    return FEEDBACK_LOG
