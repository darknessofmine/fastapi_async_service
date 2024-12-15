from pydantic import BaseModel

from api.sub_tier.schemas import SubTierResponse


class SubscriptionResponse(BaseModel):
    author_id: int
    sub_id: int
    sub_tier: SubTierResponse
