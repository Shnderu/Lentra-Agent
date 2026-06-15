import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://lentra_user:lentra_pass@localhost:5432/lentra"
)

def get_db():
    return psycopg2.connect(DATABASE_URL)
