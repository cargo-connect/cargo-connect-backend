from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.v1.schemas.order import OrderCreate, OrderOut, OrderUpdate
from app.api.v1.schemas.order_pricing import PricingBase
from app.api.v1.services import order as order_service
from app.api.v1.services.order_pricing import calculate_estimated_price
from app.api.v1.routes.user import get_current_user
from app.api.v1.models.user import User
from app.api.db.database import get_db

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.post("/", response_model=OrderOut)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return order_service.create_order(db, current_user.id, order_data)


@order_router.get("/", response_model=List[OrderOut])
def list_orders(db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return order_service.get_orders(db, current_user.id)


@order_router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = order_service.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@order_router.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, update_data: OrderUpdate,
                 db: Session = Depends(get_db)):
    updated = order_service.update_order(db, order_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated


@order_router.post("/{order_id}/estimate-price", response_model=PricingBase)
def get_estimated_price_for_order(
    order_id: int,
    delivery_type: str,
    distance: float,
    weight: float = 0
):
    estimated_price = calculate_estimated_price(
        delivery_type=delivery_type,
        distance=distance,
        weight=weight
    )
    return {"estimated_price": estimated_price}
