from lentra.core.contracts.dto import RequestDTO, ResponseDTO


class DTOEnforcer:

    @staticmethod
    def validate_request(obj):
        if not isinstance(obj.query, str):
            raise ValueError("Invalid RequestDTO: query must be string")

    @staticmethod
    def validate_response(obj):
        if obj.results is None:
            raise ValueError("Invalid ResponseDTO: results missing")
