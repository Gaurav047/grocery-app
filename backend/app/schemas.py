from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: float
    unit: str
    image_url: str
    stock: int
    category: CategoryOut


class CartItemIn(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1, le=99)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=0, le=99)


class CartItemOut(BaseModel):
    product: ProductOut
    quantity: int
    line_total: float


class CartOut(BaseModel):
    cart_id: str
    items: list[CartItemOut]
    subtotal: float
    item_count: int


class CheckoutIn(BaseModel):
    customer_name: str = Field(min_length=1, max_length=120)
    address: str = Field(min_length=1, max_length=300)


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    product_name: str
    unit_price: float
    quantity: int


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_name: str
    address: str
    total: float
    created_at: datetime
    items: list[OrderItemOut]
