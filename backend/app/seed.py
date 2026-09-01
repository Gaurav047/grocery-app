"""Populate the database with demo categories and products.

Usage: python -m app.seed
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models import Base, Category, Product

CATEGORIES = {
    "produce": "Produce",
    "dairy": "Dairy & Eggs",
    "bakery": "Bakery",
    "pantry": "Pantry",
    "beverages": "Beverages",
    "frozen": "Frozen",
}

PRODUCTS = [
    ("produce", "Bananas", "Sweet ripe bananas", 0.59, "lb", 150),
    ("produce", "Avocado", "Creamy Hass avocado", 1.49, "each", 80),
    ("produce", "Baby Spinach", "Triple-washed baby spinach", 3.29, "5 oz bag", 40),
    ("produce", "Roma Tomatoes", "Firm vine-ripened tomatoes", 1.89, "lb", 60),
    ("produce", "Red Apples", "Crisp red delicious apples", 2.19, "lb", 90),
    ("dairy", "Whole Milk", "Grade A whole milk", 3.79, "gallon", 45),
    ("dairy", "Large Eggs", "Cage-free large eggs", 4.49, "dozen", 60),
    ("dairy", "Greek Yogurt", "Plain nonfat Greek yogurt", 5.99, "32 oz", 30),
    ("dairy", "Cheddar Cheese", "Sharp cheddar block", 4.99, "8 oz", 35),
    ("bakery", "Sourdough Loaf", "Fresh-baked sourdough", 4.29, "loaf", 20),
    ("bakery", "Bagels", "Everything bagels", 3.99, "6 pack", 25),
    ("bakery", "Croissants", "All-butter croissants", 5.49, "4 pack", 18),
    ("pantry", "Olive Oil", "Extra virgin olive oil", 9.99, "500 ml", 25),
    ("pantry", "Spaghetti", "Durum wheat spaghetti", 1.79, "16 oz", 70),
    ("pantry", "Peanut Butter", "Creamy peanut butter", 3.49, "16 oz", 40),
    ("pantry", "Jasmine Rice", "Fragrant jasmine rice", 8.99, "5 lb", 30),
    ("beverages", "Orange Juice", "Not-from-concentrate OJ", 4.59, "52 oz", 28),
    ("beverages", "Cold Brew Coffee", "Smooth cold brew", 6.49, "32 oz", 22),
    ("beverages", "Sparkling Water", "Lime sparkling water", 4.99, "12 pack", 40),
    ("frozen", "Frozen Blueberries", "Wild blueberries", 5.29, "16 oz", 26),
    ("frozen", "Cheese Pizza", "Thin-crust cheese pizza", 6.99, "each", 24),
    ("frozen", "Vanilla Ice Cream", "Slow-churned vanilla", 5.79, "1.5 qt", 20),
]


def seed(db: Session) -> None:
    for slug, name in CATEGORIES.items():
        if db.scalar(select(Category).where(Category.slug == slug)) is None:
            db.add(Category(slug=slug, name=name))
    db.flush()

    categories = {c.slug: c for c in db.scalars(select(Category))}
    for slug, name, description, price, unit, stock in PRODUCTS:
        if db.scalar(select(Product).where(Product.name == name)) is not None:
            continue
        db.add(
            Product(
                name=name,
                description=description,
                price=price,
                unit=unit,
                stock=stock,
                image_url=f"https://placehold.co/400x300?text={name.replace(' ', '+')}",
                category_id=categories[slug].id,
            )
        )
    db.commit()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)
    print(f"Seeded {len(PRODUCTS)} products across {len(CATEGORIES)} categories.")


if __name__ == "__main__":
    main()
