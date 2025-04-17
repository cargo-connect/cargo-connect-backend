from sqlalchemy.orm import Session
from app.api.v1.models.order import Order, OrderStatus
from app.api.v1.schemas.order import OrderCreate, OrderUpdate
from app.api.v1.services.order_pricing import calculate_estimated_price


def create_order(db: Session, user_id: int, order_data: OrderCreate,
                 distance: float, weight: float = 0):
    estimated_price = calculate_estimated_price(
        delivery_type=order_data.delivery_type.value, distance=distance,
        weight=weight
    )
    # This stores this price in the order or returns it in the response.
    order = Order(**order_data.dict(), user_id=user_id,
                  estimated_price=estimated_price)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order, estimated_price


def get_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def update_order(db: Session, order_id: int, update_data: OrderUpdate):
    order = get_order_by_id(db, order_id)
    if not order:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order
