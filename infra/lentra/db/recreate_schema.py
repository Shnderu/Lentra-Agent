from lentra.db.session import engine, Base

# canonical property model registration
from lentra.models.storage import PropertyDB  # noqa


def reset_schema():

    Base.metadata.drop_all(bind=engine)

    Base.metadata.create_all(bind=engine)

    print("SCHEMA RECREATED")


if __name__ == "__main__":
    reset_schema()
