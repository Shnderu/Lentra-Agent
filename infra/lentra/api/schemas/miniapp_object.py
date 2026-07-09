from pydantic import BaseModel


class MiniAppObjectDetailResponseSchema(BaseModel):

    contract_version: str

    object: dict

    intelligence: dict

    verdict: dict

    explanation: dict
