from pydantic import BaseModel


class TokenInfo(BaseModel):
    asess_token: str
    token_type: str
