from lentra.connectors.mock_connector.connector import MockConnector
from lentra.connectors.telegram_connector.connector import TelegramConnector
from lentra.connectors.telegram_live.connector import TelegramLiveConnector


DOMIKO_MESSAGES = [
"""2+1, 71 кв/м
17.5 млн VND/месяц
Бассейн
Депозит: 17.5 млн VND"""
]


class ConnectorRegistry:

    @staticmethod
    def get_connectors():

        return [
            MockConnector(),
            TelegramConnector(DOMIKO_MESSAGES),
            TelegramLiveConnector()
        ]
