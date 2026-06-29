from typing import Dict, Any, List


class EngineRegistry:

    def __init__(self):

        self.engines = []

    def register(self, engine):

        self.engines.append(engine)

    def run(self, listing: dict) -> dict:

        for engine in self.engines:

            listing = engine.process(listing)

        return listing

    def run_all(self, listings: List[dict]) -> List[dict]:

        return [self.run(l) for l in listings]
