class UnifiedDedupEntry:

    def __init__(self, cluster_engine, rule_engine):
        self.cluster_engine = cluster_engine
        self.rule_engine = rule_engine

    def dedup(self, listings):

        clustered = self.cluster_engine.cluster(listings)

        return self.rule_engine.merge(clustered)
