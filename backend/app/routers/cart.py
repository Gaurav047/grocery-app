from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import CartItem, Product
from app.schemas import CartItemIn, CartItemOut, CartItemUpdate, CartOut

router = APIRouter(prefix="/cart", tags=["cart"])


def get_cart_id(x_cart_id: str = Header(..., max_length=64)) -> str:
    return x_cart_id


def build_cart(db: Session, cart_id: str) -> CartOut:
    items = db.scalars(
        select(CartItem)
        .options(joinedload(CartItem.product).joinedload(Product.category))
        .where(CartItem.cart_id == cart_id)
        .order_by(CartItem.id)
    ).all()
    out_items = [
        CartItemOut(
            product=item.product,
            quantity=item.quantity,
            line_total=round(item.product.price * item.quantity, 2),
        )
        for item in items
    ]
    return CartOut(
        cart_id=cart_id,
        items=out_items,
        subtotal=round(sum(i.line_total for i in out_items), 2),
        item_count=sum(i.quantity for i in out_items),
    )


@router.get("", response_model=CartOut)
def read_cart(cart_id: str = Depends(get_cart_id), db: Session = Depends(get_db)) -> CartOut:
    return build_cart(db, cart_id)


@router.post("/items", response_model=CartOut, status_code=201)
def add_item(
    payload: CartItemIn,
    cart_id: str = Depends(get_cart_id),
    db: Session = Depends(get_db),
) -> CartOut:
    product = db.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    item = db.scalar(
        select(CartItem).where(
            CartItem.cart_id == cart_id, CartItem.product_id == payload.product_id
        )
    )
    quantity = payload.quantity + (item.quantity if item else 0)
    if quantity > product.stock:
        raise HTTPException(status_code=409, detail="Not enough stock")

    if item is None:
        db.add(CartItem(cart_id=cart_id, product_id=payload.product_id, quantity=quantity))
    else:
        item.quantity = quantity
    db.commit()
    return build_cart(db, cart_id)


@router.patch("/items/{product_id}", response_model=CartOut)
def update_item(
    product_id: int,
    payload: CartItemUpdate,
    cart_id: str = Depends(get_cart_id),
    db: Session = Depends(get_db),
) -> CartOut:
    item = db.scalar(
        select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Item not in cart")
    if payload.quantity == 0:
        db.delete(item)
    else:
        if payload.quantity > item.product.stock:
            raise HTTPException(status_code=409, detail="Not enough stock")
        item.quantity = payload.quantity
    db.commit()
    return build_cart(db, cart_id)


@router.delete("/items/{product_id}", response_model=CartOut)
def remove_item(
    product_id: int,
    cart_id: str = Depends(get_cart_id),
    db: Session = Depends(get_db),
) -> CartOut:
    item = db.scalar(
        select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Item not in cart")
    db.delete(item)
    db.commit()
    return build_cart(db, cart_id)
