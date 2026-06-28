

from collections import defaultdict
from lentra.core.ai.feedback.store.feedback_store import get_feedback


def build_preference_weights():

    feedback = get_feedback()

    weights = defaultdict(float)

    for f in feedback:

        lid = f["listing_id"]

        if f["action"] == "click":
            weights[lid] += 2.0

        elif f["action"] == "save":
            weights[lid] += 3.0

        elif f["action"] == "reject":
            weights[lid] -= 2.5

        elif f["action"] == "ignore":
            weights[lid] -= 1.0

    return weights
