from typing import List, Dict, Any


class CandidateRepository:
    """
    Market listing candidates storage.

    Phase 1:
    - static MVP dataset

    Future:
    - Facebook
    - Telegram
    - local portals
    - agency feeds
    """

    def search(
        self,
        city: str = None
    ) -> List[Dict[str, Any]]:

        listings = [
            {
                "id": "dn001",
                "title": "Studio My Khe beach",
                "price": 700,
                "city": "da_nang",
                "source": "facebook"
            },
            {
                "id": "dn002",
                "title": "Studio near My Khe beach",
                "price": 680,
                "city": "da_nang",
                "source": "telegram"
            },
            {
                "id": "dn003",
                "title": "Apartment Da Nang center",
                "price": 550,
                "city": "da_nang",
                "source": "agency"
            }
        ]

        if city:
            return [
                item
                for item in listings
                if item["city"] == city
            ]

        return listings


candidate_repository = CandidateRepository()
