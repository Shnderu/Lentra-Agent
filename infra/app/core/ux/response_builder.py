from app.core.contracts.api_response import APIResponse


class ResponseBuilder:

    def build(self, trace_id, query, listings, total):

        items = [
            {
                "title": l.title,
                "price": l.price,
                "city": l.city,
                "source": getattr(l, "source", None)
            }
            for l in listings
        ]

        return APIResponse(
            trace_id=trace_id,
            query=query,
            total=total,
            returned=len(items),
            items=items
        )
