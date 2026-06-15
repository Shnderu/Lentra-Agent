from sqlalchemy import Column, Integer, String, Float, Boolean
from lentra.db.base import Base


class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    price_vnd_mln = Column(Float, index=True)
    deposit_vnd_mln = Column(Float)

    area_m2 = Column(Float)

    bedrooms = Column(Integer)
    bathrooms = Column(Integer)

    city = Column(String, index=True)
    district = Column(String, index=True)

    pool = Column(Boolean, default=False)
    sea_view = Column(Boolean, default=False)
    pet_friendly = Column(Boolean, default=False)

    score = Column(Float, default=0.0)
