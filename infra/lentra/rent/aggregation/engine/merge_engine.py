class MergeEngine:

    def merge(self, results: list) -> list:
        items = []

        for r in results:
            items.extend(r.get("items", []))

        return self._dedup(items)

    def _dedup(self, items: list) -> list:
        seen = set()
        out = []

        for i in items:
            key = (i.get("title"), i.get("price"))

            if key in seen:
                continue

            seen.add(key)
            out.append(i)

        return out
