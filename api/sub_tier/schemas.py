from pydantic import BaseModel


class SubTierBase(BaseModel):
    title: str
    body: str
    price: int


class SubTierCreate(SubTierBase):
    ...


class SubTierUpdate(SubTierCreate):
    ...


class SubTierUpdatePartial(SubTierUpdate):
    title: str | None = None
    body: str | None = None
    price: int | None = None


class SubTierResponse(SubTierBase):
    id: int
