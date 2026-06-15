import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="lentra",
    user="lentra_user",
    password="lentra_pass",
)

cur = conn.cursor()

cur.execute("DELETE FROM properties")

for i in range(1, 101):
    cur.execute(
        """
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
            raw,
            features
        )
        VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """,
        (
            f"Test Apartment #{i}",
            8 + (i % 15),
            8 + (i % 15),
            30 + i,
            1 + (i % 3),
            1 + (i % 2),
            True,
            i % 2 == 0,
            i % 5 == 0,
            0.5 + (i / 200),
            "{}",
            "{}",
        ),
    )

conn.commit()

cur.close()
conn.close()

print("Seed completed: 100 properties inserted")
