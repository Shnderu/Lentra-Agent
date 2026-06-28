

from collections import defaultdict


class ClusterBuilder:

    def build(self, listings: list):

        clusters = defaultdict(list)

        for l in listings:
            cluster_id = l.get("cluster_id", l["id"])
            clusters[cluster_id].append(l)

        return clusters
