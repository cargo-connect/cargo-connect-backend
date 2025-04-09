from sqlalchemy.orm import Session
from app.api.v1.models.order import Order, OrderStatus
from app.api.v1.schemas.order import OrderCreate, OrderUpdate


def create_order(db: Session, user_id: int, order_data: OrderCreate):
    order = Order(**order_data.dict(), user_id=user_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


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
