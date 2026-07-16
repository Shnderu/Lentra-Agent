from lentra.db.session import SessionLocal
from lentra.models.apartment import Apartment


def seed():
    db = SessionLocal()

    try:
        db.query(Apartment).delete()

        apartments = [
            Apartment(
                title="Sea View Premium",
                price_vnd_mln=9,
                area_m2=58,
                bedrooms=1,
                bathrooms=1,
                pool=True,
                sea_view=True,
                city="Da Nang",
                district="My An",
                score=0.0,
            ),
            Apartment(
                title="Family Pool Apartment",
                price_vnd_mln=8,
                area_m2=96,
                bedrooms=2,
                bathrooms=2,
                pool=True,
                sea_view=False,
                city="Da Nang",
                district="Binh Thanh",
                score=0.0,
            ),
            Apartment(
                title="Budget Studio",
                price_vnd_mln=5,
                area_m2=40,
                bedrooms=1,
                bathrooms=1,
                pool=False,
                sea_view=False,
                city="Da Nang",
                district="My An",
                score=0.0,
            ),
        ]

        db.add_all(apartments)
        db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    seed()
