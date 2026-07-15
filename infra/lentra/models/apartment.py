from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    JSON
)

from lentra.db.base import Base


class Apartment(Base):

    __tablename__ = "apartments"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(String)

    price_vnd_mln = Column(
        Float,
        index=True
    )

    deposit_vnd_mln = Column(
        Float
    )

    area_m2 = Column(
        Float
    )


    city = Column(
        String,
        index=True
    )

    district = Column(
        String,
        index=True
    )


    bedrooms = Column(
        Integer
    )

    bathrooms = Column(
        Integer
    )


    pool = Column(
        Boolean,
        default=False
    )

    sea_view = Column(
        Boolean,
        default=False
    )

    pet_friendly = Column(
        Boolean,
        default=False
    )


    score = Column(
        Float,
        default=0.0
    )


    source_chat_id = Column(
        Integer,
        index=True
    )

    source_message_id = Column(
        Integer,
        index=True
    )


    description = Column(
        String
    )

    property_type = Column(
        String
    )

    currency = Column(
        String,
        default="VND"
    )

    raw_text = Column(
        String
    )


    features = Column(
        JSON
    )


    electricity_price = Column(
        Float
    )

    water_price = Column(
        Float
    )


    floor = Column(
        Integer
    )

    total_floors = Column(
        Integer
    )


    balcony = Column(
        Boolean,
        default=False
    )

    elevator = Column(
        Boolean,
        default=False
    )

    parking = Column(
        Boolean,
        default=False
    )

    furnished = Column(
        Boolean,
        default=False
    )

    washing_machine = Column(
        Boolean,
        default=False
    )

    air_conditioner = Column(
        Boolean,
        default=False
    )

    kitchen = Column(
        Boolean,
        default=False
    )

    refrigerator = Column(
        Boolean,
        default=False
    )

    internet = Column(
        Boolean,
        default=False
    )

    wifi = Column(
        Boolean,
        default=False
    )
