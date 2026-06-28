

from lentra.core.data_layer.ingestion.ingestion_engine import IngestionEngine

engine = IngestionEngine()


def run_mock_feed():

    listings = [
        {
            "id": "fb-1",
            "title": "Beach studio My Khe wifi",
            "price": 650,
            "city": "Da Nang",
            "location": "My Khe",
            "source": "facebook"
        },
        {
            "id": "tg-2",
            "title": "Cheap studio near beach internet",
            "price": 400,
            "city": "Da Nang",
            "location": "My Khe",
            "source": "telegram"
        },
        {
            "id": "fb-3",
            "title": "Luxury sea view apartment wifi",
            "price": 1200,
            "city": "Da Nang",
            "location": "My Khe",
            "source": "facebook"
        }
    ]

    for l in listings:
        engine.ingest(l)


if __name__ == "__main__":
    run_mock_feed()
