from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

engine = create_engine("postgresql://postgres:postgres@127.0.0.1:5432/lentra")


@app.get("/response/{task_id}")
def get_response(task_id: int):
    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT status, result
            FROM processing_queue
            WHERE id = :id
        """), {"id": task_id}).fetchone()

    if not row:
        return {"error": "not found"}

    return {
        "status": row[0],
        "result": row[1]
    }
