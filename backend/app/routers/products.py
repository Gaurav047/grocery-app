from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Category, Product
from app.schemas import CategoryOut, ProductOut

router = APIRouter(tags=["catalog"])


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)) -> list[Category]:
    return list(db.scalars(select(Category).order_by(Category.name)))


@router.get("/products", response_model=list[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    search: str | None = Query(default=None, max_length=120),
    category: str | None = Query(default=None, max_length=80),
    limit: int = Query(default=60, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[Product]:
    stmt = select(Product).options(joinedload(Product.category)).order_by(Product.name)
    if search:
        stmt = stmt.where(Product.name.ilike(f"%{search}%"))
    if category:
        stmt = stmt.join(Category).where(Category.slug == category)
    return list(db.scalars(stmt.limit(limit).offset(offset)))


@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
