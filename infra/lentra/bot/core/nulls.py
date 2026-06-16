class NullRenderer:
    def render(self, *args, **kwargs):
        return None


class NullFSM:
    def __init__(self):
        pass


class NullStateStore:
    def get(self, *args, **kwargs):
        return None

    def set(self, *args, **kwargs):
        return None


class NullSearchService:
    def search(self, *args, **kwargs):
        return []
