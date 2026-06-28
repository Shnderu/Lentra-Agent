

USER_PROFILE = {
    "default": {
        "max_price": 700,
        "preferred_locations": ["My Khe"],
        "noise_sensitive": True,
        "internet_required": True
    }
}


def get_profile(user_id="default"):
    return USER_PROFILE.get(user_id, USER_PROFILE["default"])


def update_profile(user_id, updates: dict):

    if user_id not in USER_PROFILE:
        USER_PROFILE[user_id] = {}

    USER_PROFILE[user_id].update(updates)

    return USER_PROFILE[user_id]
