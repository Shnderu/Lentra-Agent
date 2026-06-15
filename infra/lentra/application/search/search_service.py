from lentra.domain.property.search import search_properties


class SearchService:

    def search(self, request, state=None):
        payload = {
            "text": request.query,
            "city": request.city,
            "budget_min": request.budget_min,
            "budget_max": request.budget_max,
            "location": {
                "lat": request.lat,
                "lng": request.lng
            } if request.lat and request.lng else None
        }

        results = search_properties(payload, state)

        return results
