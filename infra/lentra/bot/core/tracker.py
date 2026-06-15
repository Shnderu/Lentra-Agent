from lentra.bot.state.profile_store import ProfileStore


class BehaviorTracker:

    def __init__(self):
        self.store = ProfileStore()

    def view(self, user_id: int, item_id: str):

        profile = self.store.load(user_id)

        if item_id not in profile.viewed_items:
            profile.viewed_items.append(item_id)

        self.store.save(profile)

    def click(self, user_id: int, item_id: str):

        profile = self.store.load(user_id)

        if item_id not in profile.clicked_items:
            profile.clicked_items.append(item_id)

        self.store.save(profile)
