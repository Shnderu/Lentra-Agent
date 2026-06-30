class CanonicalSearchPipeline:

    def __init__(self, engine):
        self.engine = engine

    def run(self, query):

        listings = self.engine.fetch(query)

        listings = self.engine.normalize(listings)

        listings = self.engine.dedup(listings)

        listings = self.engine.rank(listings)

        listings = self.engine.risk(listings)

        return listings
