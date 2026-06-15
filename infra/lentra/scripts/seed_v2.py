import psycopg2
import random

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="lentra",
    user="lentra_user",
    password="lentra_pass",
)

cur = conn.cursor()

cur.execute("DELETE FROM properties")

cities = ["Da Nang", "Nha Trang", "Ho Chi Minh", "Ha Noi"]
districts = ["My An", "Son Tra", "District 1", "District 2", "Binh Thanh"]

for i in range(1, 201):
    city = random.choice(cities)

    cur.execute("""
        INSERT INTO properties (
            title,
            price_vnd_mln,
            deposit_vnd_mln,
            area_m2,
            bedrooms,
            bathrooms,
            pet_friendly,
            pool,
            sea_view,
            score,
            city,
            district,
            source,
            url
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        f"Apartment #{i}",
        random.randint(5, 30),
        random.randint(5, 30),
        random.randint(25, 120),
        random.randint(1, 3),
        random.randint(1, 2),
        random.choice([True, False]),
        random.choice([True, False]),
        random.choice([True, False]),
        round(random.random(), 3),
        city,
        random.choice(districts),
        "seed_v2",
        ""
    ))

conn.commit()
cur.close()
conn.close()

print("Seed v2 completed")
