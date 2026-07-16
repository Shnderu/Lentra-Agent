from lentra.db.session import engine, Base
from lentra.models.apartment import Apartment  # noqa

def reset_schema():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("SCHEMA RECREATED")

if __name__ == "__main__":
    reset_schema()
