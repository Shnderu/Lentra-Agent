class SourceTagging:

    @staticmethod
    def enrich(listing: dict, source: str):
        listing["source"] = source
        listing["source_weight"] = {
            "facebook": 0.7,
            "telegram": 0.6,
            "local_sites": 0.9,
            "agency": 1.0
        }.get(source, 0.5)

        return listing
