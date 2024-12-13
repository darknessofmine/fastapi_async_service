from pydantic import BaseModel


class SubTierBase(BaseModel):
    title: str
    body: str
    price: str


class SubTierCreate(SubTierBase):
    ...


class SubTierUpdate(SubTierCreate):
    ...


class SubTierResponse(SubTierBase):
    ...
