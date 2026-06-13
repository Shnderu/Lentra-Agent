from lentra.property.models import Property


class MockConnector:

    async def search(self, query: str):

        return [
            Property(
                id="1",
                source="mock",
                title="Modern apartment in Da Nang",
                url="https://example.com/property/1",
                city="Da Nang",
                price=450,
                bedrooms=2,
                bathrooms=1,
                area_m2=60,
                trust_score=90,
                photos=[],
                metadata={}
            ),
            Property(
                id="2",
                source="mock",
                title="Cheap studio near beach",
                url="https://example.com/property/2",
                city="Da Nang",
                price=300,
                bedrooms=1,
                bathrooms=1,
                area_m2=35,
                trust_score=70,
                photos=[],
                metadata={}
            )
        ]
