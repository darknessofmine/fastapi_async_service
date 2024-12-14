from pydantic import BaseModel


class SubscriptionResponse(BaseModel):
    author_id: int
    sub_id: int
