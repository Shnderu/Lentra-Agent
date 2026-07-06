import uuid


class LineageTracker:
    def __init__(self):
        self.root_id = str(uuid.uuid4())
        self.parents = {}

    def link(self, child: str, parent: str):
        self.parents[child] = parent

    def get_parent(self, node: str):
        return self.parents.get(node)

    def get_root(self):
        return self.root_id
