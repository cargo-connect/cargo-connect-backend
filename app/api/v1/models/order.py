from sqlalchemy import Column, Integer, Enum as SQLEnum, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.api.db.database import Base
from datetime import datetime
from enum import Enum as PyEnum
from app.api.v1.schemas.order import ItemCategory
from sqlalchemy import Float


class DeliveryType(str,  PyEnum):
    motorcycle = "motorcycle"
    car = "car"
    van = "van"
    pickup = "pickup"


class OrderStatus(str, PyEnum):
    confirmed = "confirmed"
    enroute = "enroute"
    delivered = "delivered"


class ItemCategory(str, PyEnum):
    documents = "documents"
    food = "food"
    clothings = "clothings"
    electronics = "electronics"
    gifts = "gifts"
    beauty = "beauty"
    accessories = "accessories"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    delivery_type = Column(SQLEnum(DeliveryType), nullable=False)
    item_category = Column(SQLEnum(ItemCategory), nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.confirmed)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    estimated_price = Column(Float, nullable=True)

    user = relationship("User", back_populates="orders", cascade="all, delete")


__all__ = ["Order"]




