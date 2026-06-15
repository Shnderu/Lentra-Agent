from lentra.domain.property.ingestion import PropertyIngestionService
from lentra.telegram.db import get_conn

def main():
    conn = get_conn()
    service = PropertyIngestionService(conn)

    raw_payload = {
        "id": "test-1",
        "source_id": "test-1",
        "source_type": "mock",
        "title": "Test Apartment",
        "description": "Simple test unit",

        "price_monthly": 500,
        "currency": "USD",
        "deposit": 500,

        "geo_lat": None,
        "geo_lng": None,

        "city": "HCMC",
        "district": "District 1",

        "bedrooms": 2,
        "bathrooms": 1,
        "area_m2": 55,

        "property_type": "apartment",

        "images": [],
        "amenities": [],

        "raw_payload": {},
        "quality_score": 1.0
    }

    result = service.ingest(raw_payload, "mock")
    print("INGEST RESULT:", result)

if __name__ == "__main__":
    main()
