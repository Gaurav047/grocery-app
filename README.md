# FreshCart — grocery shopping app

Full-stack grocery store: browse a catalog, search and filter by category, manage a cart, and check out.

- **Backend** — FastAPI + SQLAlchemy 2 + PostgreSQL (`backend/`)
- **Frontend** — React 19 + TypeScript + Vite (`frontend/`)

Carts are anonymous: the browser generates a UUID stored in `localStorage` and sends it as the
`X-Cart-Id` header, so no login is required.

## Quick start

Start Postgres and the API with Docker (the API seeds demo products on boot):

```bash
docker compose up --build
```

Then run the frontend:

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
```

## Running the backend without Docker

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env          # point DATABASE_URL at your Postgres
python -m app.seed
uvicorn app.main:app --reload  # http://localhost:8000/docs
```

## API

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/health` | Health check |
| GET | `/api/categories` | List categories |
| GET | `/api/products?search=&category=` | List/search products |
| GET | `/api/products/{id}` | Product detail |
| GET | `/api/cart` | Current cart (needs `X-Cart-Id`) |
| POST | `/api/cart/items` | Add product to cart |
| PATCH | `/api/cart/items/{product_id}` | Set quantity (0 removes) |
| DELETE | `/api/cart/items/{product_id}` | Remove item |
| POST | `/api/orders` | Check out the cart |
| GET | `/api/orders` | Orders for this cart |

## Checks

```bash
cd backend  && ruff check . && ruff format --check . && pytest    # tests run on SQLite
cd frontend && npm run lint && npm run build
```
