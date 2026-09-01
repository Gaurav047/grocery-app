from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import CartItem, Order, OrderItem
from app.routers.cart import get_cart_id
from app.schemas import CheckoutIn, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=201)
def create_order(
    payload: CheckoutIn,
    cart_id: str = Depends(get_cart_id),
    db: Session = Depends(get_db),
) -> Order:
    items = db.scalars(
        select(CartItem)
        .options(joinedload(CartItem.product))
        .where(CartItem.cart_id == cart_id)
        .order_by(CartItem.id)
    ).all()
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in items:
        if item.quantity > item.product.stock:
            raise HTTPException(status_code=409, detail=f"Not enough stock for {item.product.name}")

    order = Order(
        cart_id=cart_id,
        customer_name=payload.customer_name,
        address=payload.address,
        total=round(sum(i.product.price * i.quantity for i in items), 2),
        items=[
            OrderItem(
                product_id=item.product_id,
                product_name=item.product.name,
                unit_price=item.product.price,
                quantity=item.quantity,
            )
            for item in items
        ],
    )
    for item in items:
        item.product.stock -= item.quantity
        db.delete(item)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=list[OrderOut])
def list_orders(cart_id: str = Depends(get_cart_id), db: Session = Depends(get_db)) -> list[Order]:
    stmt = (
        select(Order)
        .options(joinedload(Order.items))
        .where(Order.cart_id == cart_id)
        .order_by(Order.created_at.desc())
    )
    return list(db.scalars(stmt).unique())


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)) -> Order:
    order = db.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
