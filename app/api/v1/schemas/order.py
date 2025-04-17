from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class DeliveryType(str, Enum):
    motorcycle = "motorcycle"
    car = "car"
    van = "van"
    # pickup = "pickup"


class ItemCategory(str, Enum):
    documents = "documents"
    food = "food"
    clothings = "clothings"
    electronics = "electronics"
    gifts = "gifts"
    beauty = "beauty"
    accessories = "accessories"


class OrderStatus(str, Enum):
    confirmed = "confirmed"
    enroute = "enroute"
    delivered = "delivered"


class OrderBase(BaseModel):
    delivery_type: DeliveryType
    item_category: ItemCategory


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus]
    is_completed: Optional[bool]


class OrderOut(OrderBase):
    id: int
    status: OrderStatus
    is_completed: bool
    created_at: datetime
    user_id: int
    item_category: ItemCategory
    estimated_price: Optional[float]

    class Config:
        from_attributes = True
