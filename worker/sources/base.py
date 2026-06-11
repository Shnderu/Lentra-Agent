class BaseSource:
    name = "base"

    def search(self, query: dict):
        raise NotImplementedError
