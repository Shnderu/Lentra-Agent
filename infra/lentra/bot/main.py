from lentra.bot.connectors.default_connector import DefaultConnector


def main():
    print("[BOOT] ENTER MAIN")

    connector = DefaultConnector()

    print("[BOOT] CONNECTOR READY")

    result = connector.search(
        {
            "text": "rent apartment",
            "user_id": 123,
        }
    )

    print("[RESULT]", result)

    print("[BOOT] EXIT")


if __name__ == "__main__":
    main()
