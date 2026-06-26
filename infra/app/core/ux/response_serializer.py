from lentra.core.contracts.api_response import APIResponse


class ResponseSerializer:

    def serialize(self, trace_id, payload):

        listings = payload["listings"]

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
            query=payload["query"],
            total=payload["total"],
            returned=len(items),
            items=items
        )
