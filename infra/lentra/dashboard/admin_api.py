from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

engine = create_engine(
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)


@app.get("/admin/stats")
def stats():
    with engine.begin() as conn:
        users = conn.execute(text("SELECT COUNT(*) FROM user_profiles")).fetchone()[0]
        props = conn.execute(text("SELECT COUNT(*) FROM properties")).fetchone()[0]
        queue = conn.execute(text("SELECT COUNT(*) FROM processing_queue WHERE status='new'")).fetchone()[0]

    return {
        "users": users,
        "properties": props,
        "queue": queue
    }
