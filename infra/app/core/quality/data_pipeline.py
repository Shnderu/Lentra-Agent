from lentra.core.quality.data_normalizer import DataNormalizer
from lentra.core.quality.deduplicator import Deduplicator


class DataPipeline:

    def __init__(self):
        self.normalizer = DataNormalizer()
        self.deduplicator = Deduplicator()

    def process(self, listings):

        cleaned = []

        # -------------------------
        # normalize
        # -------------------------
        for l in listings:
            norm = self.normalizer.normalize(l)
            if norm:
                cleaned.append(norm)

        # -------------------------
        # deduplicate
        # -------------------------
        cleaned = self.deduplicator.deduplicate(cleaned)

        return cleaned
