class ConnectorContractError(Exception):
    pass


class BaseConnector:

    async def call(self, query: dict) -> dict:
        raise NotImplementedError("Connector must implement async call()")
