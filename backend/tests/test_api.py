from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    assert client.get("/api/health").json() == {"status": "ok"}


def test_list_categories_and_products(client: TestClient) -> None:
    categories = client.get("/api/categories").json()
    assert {c["slug"] for c in categories} >= {"produce", "dairy", "bakery"}

    products = client.get("/api/products").json()
    assert len(products) > 0
    assert products[0]["category"]["slug"]


def test_search_and_filter_products(client: TestClient) -> None:
    found = client.get("/api/products", params={"search": "milk"}).json()
    assert [p["name"] for p in found] == ["Whole Milk"]

    produce = client.get("/api/products", params={"category": "produce"}).json()
    assert produce and all(p["category"]["slug"] == "produce" for p in produce)


def test_get_product_not_found(client: TestClient) -> None:
    assert client.get("/api/products/99999").status_code == 404


def test_cart_flow(client: TestClient) -> None:
    product = client.get("/api/products").json()[0]

    cart = client.post("/api/cart/items", json={"product_id": product["id"], "quantity": 2}).json()
    assert cart["item_count"] == 2
    assert cart["subtotal"] == round(product["price"] * 2, 2)

    cart = client.post("/api/cart/items", json={"product_id": product["id"], "quantity": 1}).json()
    assert cart["item_count"] == 3

    cart = client.patch(f"/api/cart/items/{product['id']}", json={"quantity": 1}).json()
    assert cart["item_count"] == 1

    cart = client.delete(f"/api/cart/items/{product['id']}").json()
    assert cart["items"] == []


def test_cart_rejects_over_stock(client: TestClient) -> None:
    product = client.get("/api/products").json()[0]
    response = client.post("/api/cart/items", json={"product_id": product["id"], "quantity": 99})
    assert response.status_code == 409


def test_cart_is_scoped_per_cart_id(client: TestClient) -> None:
    product = client.get("/api/products").json()[0]
    client.post("/api/cart/items", json={"product_id": product["id"], "quantity": 1})

    other = client.get("/api/cart", headers={"X-Cart-Id": "someone-else"}).json()
    assert other["items"] == []


def test_checkout_creates_order_and_clears_cart(client: TestClient) -> None:
    product = client.get("/api/products").json()[0]
    client.post("/api/cart/items", json={"product_id": product["id"], "quantity": 2})

    response = client.post(
        "/api/orders", json={"customer_name": "Gaurav", "address": "1 Market St"}
    )
    assert response.status_code == 201
    order = response.json()
    assert order["total"] == round(product["price"] * 2, 2)
    assert order["items"][0]["quantity"] == 2

    assert client.get("/api/cart").json()["items"] == []
    assert client.get("/api/products/{}".format(product["id"])).json()["stock"] == (
        product["stock"] - 2
    )
    assert [o["id"] for o in client.get("/api/orders").json()] == [order["id"]]


def test_checkout_empty_cart(client: TestClient) -> None:
    response = client.post("/api/orders", json={"customer_name": "A", "address": "B"})
    assert response.status_code == 400
