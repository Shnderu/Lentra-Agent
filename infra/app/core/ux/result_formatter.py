from app.core.contracts.response_dto import RentResponseDTO


class ResultFormatter:

    def format(self, response: RentResponseDTO, options):

        listings = response.listings

        # -------------------------
        # SORTING
        # -------------------------
        if options.sort_by == "price":
            listings = sorted(listings, key=lambda x: x.price or 10**9)

        # -------------------------
        # PAGINATION
        # -------------------------
        start = options.offset
        end = options.offset + options.limit

        listings = listings[start:end]

        return {
            "query": response.query,
            "total": response.total,
            "returned": len(listings),
            "listings": [
                {
                    "title": l.title,
                    "price": l.price,
                    "city": l.city,
                    "source": l.source
                }
                for l in listings
            ]
        }
