from pydantic import BaseModel


class SubTierBase(BaseModel):
    title: str
    body: str
    price: str


class CreateSubTier(SubTierBase):
    ...


class UpdateSubTier(CreateSubTier):
    ...


class SubTierResponse(SubTierBase):
    ...
