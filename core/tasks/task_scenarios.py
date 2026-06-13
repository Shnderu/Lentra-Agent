"""
TASK SCENARIOS (Lentra Core Contract)

Это не код выполнения — это контракт системы.
"""

SCENARIOS = {

    "route_search": {
        "description": "Поиск маршрутов / авиабилетов",
        "input": {
            "user_id": "int",
            "from": "str",
            "to": "str",
            "date": "str"
        },
        "output": {
            "routes": "list",
            "price": "float"
        }
    },

    "notify_user": {
        "description": "Отправка уведомлений пользователю",
        "input": {
            "user_id": "int",
            "message": "str"
        },
        "output": {
            "sent": "bool"
        }
    },

    "alert_engine": {
        "description": "Система алертов / событий",
        "input": {
            "event_type": "str",
            "payload": "dict"
        },
        "output": {
            "triggered": "bool"
        }
    }
}
