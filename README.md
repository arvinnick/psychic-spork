# Smart Kitchen Inventory & Predictive Replenishment System

**Live Demo:** [https://psychic-spork.onrender.com](https://psychic-spork.onrender.com)

> An intelligent inventory management system designed to eliminate human error in kitchen operations through real-time tracking and predictive ordering.

---

## What's Working Now

✅ **Core API** – FastAPI-based REST endpoints for CRUD operations  
✅ **Database Layer** – SQLAlchemy ORM with async support (SQLite for dev, PostgreSQL for prod)  
✅ **Data Models** – Inventory, Suppliers, Orders, and Loss tracking  
✅ **Async Operations** – Non-blocking database access with `asyncpg` and `aiosqlite`  

---

## Architecture

### System Design

The system operates on a **feedback loop** that learns from past behavior to predict future needs:

1. **Sensing** – Weight scales transmit real-time ingredient quantities
2. **Processing** – The system compares current stock against predicted consumption for the next delivery cycle
3. **Refining** – Loss logs are analyzed; over-ordering penalties are applied to prevent waste
4. **Execution** – Autonomous replenishment orders are triggered when inventory approaches safety thresholds (accounting for delivery latency)

### Core Concept: "The Predictive Brain"

Instead of static reorder points, the system uses **dynamic coefficients** that adapt based on outcomes:

- **Waste detected** → Coefficient decreases (reduce future orders)
- **Shortages occur** → Coefficient increases (order more)
- **Lead time factored in** → Orders trigger early enough to account for delivery delays

**Primary Optimization Goal:** Minimize residual average inventory over a 3-month rolling window while preventing stockouts.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI (Python 3.11+) |
| **Async Runtime** | Uvicorn, asyncio |
| **ORM** | SQLAlchemy 2.x (async) |
| **Dev Database** | SQLite |
| **Prod Database** | PostgreSQL |
| **Async Drivers** | `asyncpg`, `aiosqlite` |
| **Data Validation** | Pydantic 2.x |
| **Testing** | pytest, pytest-asyncio |
| **Phone Numbers** | phonenumbers library |

### Dependencies

```
fastapi[standard]
pydantic
pytest
pytest-asyncio
httpx
uvicorn
sqlalchemy
pydantic-extra-types
phonenumbers
setuptools
pytest-freezegun
aiosqlite
asyncpg
sqlalchemy[asyncio]
pydantic-settings
```

---

## Data Model

```
Inventory
├── id (PK)
├── name (unique)
├── quantity
└── suppliers (M:M relationship)

Supplier
├── id (PK)
├── name
├── address
├── number
├── email
└── inventories (M:M relationship)

Orders
├── id (PK)
├── date_time
├── quantity
├── ingredient_id (FK → Inventory)
├── supplier_id (FK → Supplier)
└── [pending: confirmed_at, delivery_date]

Losses
├── id (PK)
├── date_time
├── ingredient_id (FK → Inventory)
├── quantity
└── ingredient (relationship)
```

---

## Planned Features

**Key Initiatives:**
- **Authentication & Authorization** – Role-based access control, privilege assignment
- **Order Management** – Delivery tracking, order confirmation, post-delivery inventory updates
- **Loss Processing** – Automated deduction of losses from inventory
- **Scale Integration** – Mock scale for development, real-time weight streaming
- **Warning System** – Low-stock and shortage alerts
- **Predictive Engine** – Dynamic coefficient calculations and autonomous ordering
- **Documentation** – API docs and setup guides for all endpoints
- **Testing** – Unit tests for all CRUD operations
- **DevOps** – Dockerization, production database configuration

See the [Issues tab](https://github.com/arvinnick/psychic-spork/issues) for the full roadmap.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Virtual environment (`venv` or `poetry`)
- PostgreSQL (optional, for production)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/arvinnick/psychic-spork.git
   cd psychic-spork
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database** (SQLite for development)
   ```bash
   python app/db/models.py
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Visit: `http://localhost:8000`

### Environment Variables

Create a `.env` file in the root directory:

```env
DEBUG=True
DATABASE_URL=sqlite:///./test.db
```

For production (PostgreSQL):
```env
DEBUG=False
DATABASE_URL=postgresql+asyncpg://user:password@localhost/psychic_spork
```

---

## API Endpoints

### Inventory
- `GET /inventory` – List all ingredients
- `POST /inventory` – Create new ingredient
- `PUT /inventory/{id}` – Update ingredient quantity
- `DELETE /inventory/{id}` – Remove ingredient

### Suppliers
- `GET /suppliers` – List all suppliers
- `POST /suppliers` – Add new supplier
- `PUT /suppliers/{id}` – Update supplier info
- `DELETE /suppliers/{id}` – Remove supplier

### Orders
- `GET /orders` – List all orders
- `POST /orders` – Create new order
- `PUT /orders/{id}` – Update order
- `DELETE /orders/{id}` – Cancel order

### Losses
- `GET /losses` – View recorded waste/losses
- `POST /losses` – Log ingredient loss
- `DELETE /losses/{id}` – Remove loss record

---

## Current Status

**Phase:** MVP Development (Core infrastructure in place)

**Known Issues:**
- GET `/losses` endpoint has bugs (see [#59](https://github.com/arvinnick/psychic-spork/issues/59))
- Dependency injection needs fixes (see [#55](https://github.com/arvinnick/psychic-spork/issues/55))

**Next Priorities:**
1. Fix critical bugs in losses endpoint
2. Implement authentication system
3. Add order delivery tracking
4. Deploy scale integration

---

## Contributing

This project is under active development. Check the [Issues](https://github.com/arvinnick/psychic-spork/issues) tab for tasks or features you'd like to work on.

---

## License

Apache License 2.0 – See [LICENSE](LICENSE) file for details

---

## Related Resources

- **Project Board:** [See planned work](https://github.com/arvinnick/psychic-spork/issues)
- **Live Instance:** [https://psychic-spork.onrender.com](https://psychic-spork.onrender.com)
- **Concept:** Smart, adaptive inventory management inspired by machine learning feedback loops
