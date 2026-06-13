from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://lentra_user:lentra_pass@localhost:5432/lentra"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def compute_score(p, user=None):
    score = 0.0

    if p.area_m2:
        score += min(p.area_m2 / 10, 10)

    if p.bedrooms:
        score += p.bedrooms * 2

    if p.bathrooms:
        score += p.bathrooms * 1.5

    if p.sea_view:
        score += 5 if not user or user.get("prefers_sea_view") else 8

    if p.pool:
        score += 3

    if p.pet_friendly:
        score += 2

    if p.price_vnd_mln:
        score -= p.price_vnd_mln * 0.5

        if user:
            if p.price_vnd_mln < user.get("min_price", 0):
                score -= 5
            if p.price_vnd_mln > user.get("max_price", 999999):
                score -= 10

    return round(score, 2)


def get_feed(limit=20, user=None):
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT *
            FROM properties
        """)).fetchall()

    results = []

    for r in rows:
        class P: pass

        p = P()
        p.area_m2 = r.area_m2
        p.bedrooms = r.bedrooms
        p.bathrooms = r.bathrooms
        p.price_vnd_mln = r.price_vnd_mln
        p.pet_friendly = r.pet_friendly
        p.pool = r.pool
        p.sea_view = r.sea_view

        results.append({
            "id": r.id,
            "title": r.title,
            "score": compute_score(p, user),
            "price_vnd_mln": r.price_vnd_mln,
            "area_m2": r.area_m2,
            "bedrooms": r.bedrooms,
            "bathrooms": r.bathrooms
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:limit]
