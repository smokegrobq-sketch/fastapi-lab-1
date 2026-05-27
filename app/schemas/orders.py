from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int


class OrderBase(BaseModel):
    user_id: int
    status: str = Field(default="new", min_length=2, max_length=30)


class OrderCreate(OrderBase):
    items: list[OrderItemCreate] = Field(default_factory=list)


class OrderUpdate(BaseModel):
    user_id: int | None = None
    status: str | None = Field(default=None, min_length=2, max_length=30)


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    items: list[OrderItemRead] = Field(default_factory=list)
