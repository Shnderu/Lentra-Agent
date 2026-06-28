from lentra.core.models.listing import Listing


def fetch_listings(query: dict):

    return [
        Listing(
            id="1",
            title="Studio near beach",
            price=700,
            currency="USD",
            location=query.get("city", "unknown"),
            source="mock"
        ),
        Listing(
            id="2",
            title="Modern apartment center",
            price=650,
            currency="USD",
            location=query.get("city", "unknown"),
            source="mock"
        )
    ]
