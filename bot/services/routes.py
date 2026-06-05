from core.db_init import get_conn
from core.event_bus import publish


def add_route(user_id, route):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO routes (user_id, route) VALUES (%s, %s)",
        (user_id, route)
    )

    conn.commit()
    cur.close()
    conn.close()

    publish("route_created", {"user_id": user_id, "route": route})


def get_routes(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT route FROM routes WHERE user_id=%s",
        (user_id,)
    )

    data = cur.fetchall()

    cur.close()
    conn.close()

    return [d[0] for d in data]


def delete_routes(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM routes WHERE user_id=%s",
        (user_id,)
    )

    conn.commit()
    cur.close()
    conn.close()

    publish("route_deleted", {"user_id": user_id})
