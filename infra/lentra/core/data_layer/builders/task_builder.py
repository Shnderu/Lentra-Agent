
class TaskBuilder:

    def build(self, raw_listing):

        return {
            "text": self._to_query(raw_listing),
            "source": raw_listing.get("raw"),
            "meta": {
                "price": raw_listing.get("price"),
                "location": raw_listing.get("location"),
                "title": raw_listing.get("title")
            }
        }

    def _to_query(self, r):
        return f"{r.get('title')} in {r.get('location')} for {r.get('price')}"
