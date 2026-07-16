from lentra.db.session import SessionLocal
from lentra.models.storage import PropertyDB


def seed():

    db = SessionLocal()

    try:

        db.query(PropertyDB).delete()


        properties = [

            PropertyDB(
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
                source="seed",
                raw="seed data"
            ),


            PropertyDB(
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
                source="seed",
                raw="seed data"
            ),


            PropertyDB(
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
                source="seed",
                raw="seed data"
            ),
        ]


        db.add_all(properties)

        db.commit()


    finally:

        db.close()


if __name__ == "__main__":
    seed()
