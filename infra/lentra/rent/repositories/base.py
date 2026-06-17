class BaseRepository:
    def __init__(self, provider, trace=None):
        self.provider = provider
        self.trace = trace
