# AI Native Full Stack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the FastAPI + SQLAlchemy 2.0 Async backend for the AI terminal company website, connect it to the already-implemented Vue3 frontend, and verify the full stack works end-to-end.

**Architecture:** Pure FastAPI backend with layered structure (api → crud → db). SQLAlchemy 2.0 Async ORM with aiosqlite driver. Alembic for migrations. No Django. Frontend is already complete — only proxy port fix required.

**Tech Stack:** Python 3.11+, FastAPI 0.115+, SQLAlchemy 2.0 Async, aiosqlite, Alembic, pydantic-settings 2.x, pytest + pytest-asyncio + httpx; Vue3 (already built)

**Conda environment:** `ai-full-stack` — activate before every step: `conda activate ai-full-stack`

---

## File Map

Files to **create** (backend):

| File | Responsibility |
|------|---------------|
| `backend/pyproject.toml` | Dependencies + pytest config |
| `backend/.env` | Local environment variables |
| `backend/alembic.ini` | Alembic CLI config |
| `backend/alembic/env.py` | Async migration runner |
| `backend/app/__init__.py` | Package marker |
| `backend/app/main.py` | FastAPI app factory, CORS, router registration |
| `backend/app/core/__init__.py` | Package marker |
| `backend/app/core/config.py` | pydantic-settings Settings class |
| `backend/app/db/__init__.py` | Package marker |
| `backend/app/db/base.py` | SQLAlchemy DeclarativeBase |
| `backend/app/db/session.py` | AsyncEngine + async_session_factory |
| `backend/app/api/__init__.py` | Package marker |
| `backend/app/api/deps.py` | `get_db` dependency injection |
| `backend/app/api/v1/__init__.py` | Aggregates all v1 routers |
| `backend/app/api/v1/endpoints/__init__.py` | Package marker |
| `backend/app/api/v1/endpoints/products.py` | GET /products, GET /products/{slug} |
| `backend/app/api/v1/endpoints/contact.py` | POST /contact |
| `backend/app/api/v1/endpoints/stats.py` | GET /stats |
| `backend/app/models/__init__.py` | Package marker |
| `backend/app/models/domain/__init__.py` | Package marker |
| `backend/app/models/domain/product.py` | Product, Feature, Spec, Image, SiteStat ORM models |
| `backend/app/models/domain/contact.py` | ContactSubmission ORM model |
| `backend/app/models/schemas/__init__.py` | Package marker |
| `backend/app/models/schemas/product.py` | Pydantic response schemas |
| `backend/app/models/schemas/contact.py` | Pydantic ContactIn / ContactOut |
| `backend/app/crud/__init__.py` | Package marker |
| `backend/app/crud/product_crud.py` | DB queries for products + stats |
| `backend/app/crud/contact_crud.py` | DB insert for contact submissions |
| `backend/tests/__init__.py` | Package marker |
| `backend/tests/conftest.py` | Async test fixtures (db + http client) |
| `backend/tests/test_products.py` | Product endpoint tests |
| `backend/tests/test_contact.py` | Contact endpoint tests |
| `backend/tests/test_stats.py` | Stats endpoint tests |
| `backend/scripts/__init__.py` | Package marker |
| `backend/scripts/seed_data.py` | Populates initial product + stats data |

Files to **modify**:

| File | Change |
|------|--------|
| `backend/` | Remove `requirements.txt` (replaced by pyproject.toml) |
| `frontend/vite.config.ts` | Fix proxy target from `:8080` → `:8000` |

---

## Task 1: Project Structure + pyproject.toml

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/.env`
- Delete: `backend/requirements.txt`
- Create: all `__init__.py` package markers

- [ ] **Step 1: Activate conda environment**

```bash
conda activate ai-full-stack
```

- [ ] **Step 2: Create backend directory skeleton**

```bash
cd d:/Code/python/ai-native-full-stack/backend
mkdir -p app/api/v1/endpoints app/core app/crud app/db app/models/domain app/models/schemas app/services alembic scripts tests
```

- [ ] **Step 3: Create all __init__.py package markers**

```bash
touch app/__init__.py app/api/__init__.py app/api/v1/__init__.py app/api/v1/endpoints/__init__.py app/core/__init__.py app/crud/__init__.py app/db/__init__.py app/models/__init__.py app/models/domain/__init__.py app/models/schemas/__init__.py app/services/__init__.py scripts/__init__.py tests/__init__.py
```

- [ ] **Step 4: Create pyproject.toml**

Create `backend/pyproject.toml`:

```toml
[project]
name = "ai-native-backend"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "sqlalchemy[asyncio]>=2.0.0",
    "aiosqlite>=0.20.0",
    "alembic>=1.13.0",
    "pydantic>=2.8.0",
    "pydantic-settings>=2.4.0",
    "python-dotenv>=1.0.1",
    "email-validator>=2.2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",
]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[tool.setuptools.packages.find]
where = ["."]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

- [ ] **Step 5: Create .env**

Create `backend/.env`:

```
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3
CORS_ORIGINS=["http://localhost:5173"]
```

- [ ] **Step 6: Remove old requirements.txt and install deps**

```bash
rm requirements.txt
pip install -e ".[dev]"
```

Expected: installs fastapi, sqlalchemy, aiosqlite, alembic, pytest, httpx and all other deps.

- [ ] **Step 7: Commit**

```bash
cd d:/Code/python/ai-native-full-stack
git init
git add backend/pyproject.toml backend/.env backend/app/ backend/scripts/ backend/tests/ backend/alembic/
git commit -m "chore: initialize backend project structure with pyproject.toml"
```

---

## Task 2: Core Config

**Files:**
- Create: `backend/app/core/config.py`

- [ ] **Step 1: Create config.py**

Create `backend/app/core/config.py`:

```python
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"
    DATABASE_URL: str = "sqlite+aiosqlite:///./db.sqlite3"
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    model_config = {"env_file": ".env"}


settings = Settings()
```

- [ ] **Step 2: Verify import works**

```bash
cd d:/Code/python/ai-native-full-stack/backend
python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
```

Expected output: `sqlite+aiosqlite:///./db.sqlite3`

- [ ] **Step 3: Commit**

```bash
git add backend/app/core/config.py
git commit -m "feat: add pydantic-settings config"
```

---

## Task 3: Database Base + Session

**Files:**
- Create: `backend/app/db/base.py`
- Create: `backend/app/db/session.py`

- [ ] **Step 1: Create db/base.py**

Create `backend/app/db/base.py`:

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

- [ ] **Step 2: Create db/session.py**

Create `backend/app/db/session.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False},
)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
```

- [ ] **Step 3: Verify import**

```bash
python -c "from app.db.session import async_session_factory; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add backend/app/db/
git commit -m "feat: add SQLAlchemy async engine and session factory"
```

---

## Task 4: Domain Models

**Files:**
- Create: `backend/app/models/domain/product.py`
- Create: `backend/app/models/domain/contact.py`

- [ ] **Step 1: Create product domain models**

Create `backend/app/models/domain/product.py`:

```python
from datetime import datetime
from sqlalchemy import String, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id          : Mapped[int]      = mapped_column(primary_key=True, autoincrement=True)
    slug        : Mapped[str]      = mapped_column(String(50), unique=True, index=True)
    category    : Mapped[str]      = mapped_column(String(20))
    name        : Mapped[str]      = mapped_column(String(100))
    tagline     : Mapped[str]      = mapped_column(String(200))
    description : Mapped[str]      = mapped_column(Text)
    cover_image : Mapped[str]      = mapped_column(String(500))
    is_active   : Mapped[bool]     = mapped_column(Boolean, default=True)
    sort_order  : Mapped[int]      = mapped_column(Integer, default=0)
    created_at  : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at  : Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    features : Mapped[list["ProductFeature"]] = relationship(
        back_populates="product",
        order_by="ProductFeature.sort_order",
        cascade="all, delete-orphan",
    )
    specs    : Mapped[list["ProductSpec"]]    = relationship(
        back_populates="product",
        order_by="ProductSpec.sort_order",
        cascade="all, delete-orphan",
    )
    images   : Mapped[list["ProductImage"]]   = relationship(
        back_populates="product",
        order_by="ProductImage.sort_order",
        cascade="all, delete-orphan",
    )


class ProductFeature(Base):
    __tablename__ = "product_features"

    id          : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id  : Mapped[int] = mapped_column(ForeignKey("products.id"))
    icon        : Mapped[str] = mapped_column(String(100))
    title       : Mapped[str] = mapped_column(String(100))
    description : Mapped[str] = mapped_column(String(300))
    sort_order  : Mapped[int] = mapped_column(Integer, default=0)

    product : Mapped["Product"] = relationship(back_populates="features")


class ProductSpec(Base):
    __tablename__ = "product_specs"

    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    spec_key   : Mapped[str] = mapped_column(String(100))
    spec_value : Mapped[str] = mapped_column(String(200))
    sort_order : Mapped[int] = mapped_column(Integer, default=0)

    product : Mapped["Product"] = relationship(back_populates="specs")


class ProductImage(Base):
    __tablename__ = "product_images"

    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    image_url  : Mapped[str] = mapped_column(String(500))
    alt_text   : Mapped[str] = mapped_column(String(200), default="")
    sort_order : Mapped[int] = mapped_column(Integer, default=0)

    product : Mapped["Product"] = relationship(back_populates="images")


class SiteStat(Base):
    __tablename__ = "site_stats"

    id         : Mapped[int]  = mapped_column(primary_key=True, autoincrement=True)
    label      : Mapped[str]  = mapped_column(String(100))
    value      : Mapped[str]  = mapped_column(String(50))
    unit       : Mapped[str]  = mapped_column(String(50), default="")
    sort_order : Mapped[int]  = mapped_column(Integer, default=0)
    is_active  : Mapped[bool] = mapped_column(Boolean, default=True)
```

- [ ] **Step 2: Create contact domain model**

Create `backend/app/models/domain/contact.py`:

```python
from datetime import datetime
from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class ContactSubmission(Base):
    __tablename__ = "contact_submissions"

    id           : Mapped[int]        = mapped_column(primary_key=True, autoincrement=True)
    name         : Mapped[str]        = mapped_column(String(100))
    email        : Mapped[str]        = mapped_column(String(254))
    company      : Mapped[str]        = mapped_column(String(200), default="")
    inquiry_type : Mapped[str]        = mapped_column(String(20), default="other")
    message      : Mapped[str]        = mapped_column(Text)
    status       : Mapped[str]        = mapped_column(String(20), default="pending")
    ip_address   : Mapped[str | None] = mapped_column(String(45), nullable=True)
    submitted_at : Mapped[datetime]   = mapped_column(DateTime, default=datetime.utcnow)
    updated_at   : Mapped[datetime]   = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    notes        : Mapped[str]        = mapped_column(Text, default="")
```

- [ ] **Step 3: Verify models import**

```bash
python -c "from app.models.domain.product import Product, SiteStat; from app.models.domain.contact import ContactSubmission; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add backend/app/models/domain/
git commit -m "feat: add SQLAlchemy domain models (Product, SiteStat, ContactSubmission)"
```

---

## Task 5: Alembic Setup + First Migration

**Files:**
- Modify: `backend/alembic.ini` (generated then edited)
- Modify: `backend/alembic/env.py` (generated then replaced)

- [ ] **Step 1: Initialize alembic**

```bash
cd d:/Code/python/ai-native-full-stack/backend
alembic init alembic
```

Expected: creates `alembic.ini` and `alembic/` directory.

- [ ] **Step 2: Replace alembic/env.py with async-compatible version**

Replace the entire contents of `backend/alembic/env.py` with:

```python
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import all models so they are registered with Base.metadata
from app.models.domain.product import Product, ProductFeature, ProductSpec, ProductImage, SiteStat  # noqa: F401
from app.models.domain.contact import ContactSubmission  # noqa: F401
from app.db.base import Base
from app.core.config import settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override sqlalchemy.url with the value from our settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- [ ] **Step 3: Generate first migration**

```bash
alembic revision --autogenerate -m "init"
```

Expected: creates `alembic/versions/xxxx_init.py` with tables for products, product_features, product_specs, product_images, site_stats, contact_submissions.

- [ ] **Step 4: Apply migration**

```bash
alembic upgrade head
```

Expected: `Running upgrade  -> xxxx, init`

- [ ] **Step 5: Verify tables created**

```bash
python -c "
import sqlite3
conn = sqlite3.connect('db.sqlite3')
tables = conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()
print([t[0] for t in tables])
"
```

Expected output includes: `products`, `product_features`, `product_specs`, `product_images`, `site_stats`, `contact_submissions`

- [ ] **Step 6: Commit**

```bash
git add backend/alembic.ini backend/alembic/
git commit -m "feat: add alembic async migrations and create initial schema"
```

---

## Task 6: FastAPI App Skeleton

**Files:**
- Create: `backend/app/api/deps.py`
- Create: `backend/app/api/v1/__init__.py`
- Create: `backend/app/main.py`

- [ ] **Step 1: Create api/deps.py**

Create `backend/app/api/deps.py`:

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
```

- [ ] **Step 2: Create app/api/v1/__init__.py (router aggregator)**

Create `backend/app/api/v1/__init__.py`:

```python
from fastapi import APIRouter

api_router = APIRouter()

# Routers are registered here after each endpoint module is created
# (populated incrementally in Tasks 7-9)
```

- [ ] **Step 3: Create app/main.py skeleton**

Create `backend/app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router

app = FastAPI(
    title="AI智能终端官网 API",
    version="2.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
```

- [ ] **Step 4: Verify app starts**

```bash
uvicorn app.main:app --port 8000 &
sleep 2
curl http://localhost:8000/api/docs
# Press Ctrl+C or kill the background process after
```

Expected: returns HTML (Swagger UI).

- [ ] **Step 5: Commit**

```bash
git add backend/app/api/deps.py backend/app/api/v1/__init__.py backend/app/main.py
git commit -m "feat: add FastAPI app skeleton with CORS and empty v1 router"
```

---

## Task 7: Test Infrastructure (conftest)

**Files:**
- Create: `backend/tests/conftest.py`

- [ ] **Step 1: Create conftest.py**

Create `backend/tests/conftest.py`:

```python
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.main import app
from app.api.deps import get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncClient:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()
```

- [ ] **Step 2: Run pytest to confirm fixtures load**

```bash
pytest tests/ -v
```

Expected: `no tests ran`, no import errors.

- [ ] **Step 3: Commit**

```bash
git add backend/tests/conftest.py
git commit -m "test: add async test fixtures with in-memory SQLite"
```

---

## Task 8: [TDD] Products Endpoint

**Files:**
- Create: `backend/tests/test_products.py`
- Create: `backend/app/models/schemas/product.py`
- Create: `backend/app/crud/product_crud.py`
- Create: `backend/app/api/v1/endpoints/products.py`
- Modify: `backend/app/api/v1/__init__.py`

- [ ] **Step 1: Write failing tests**

Create `backend/tests/test_products.py`:

```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain.product import Product, ProductFeature, ProductSpec, ProductImage


@pytest.mark.asyncio
async def test_list_products_empty(client: AsyncClient):
    response = await client.get("/api/v1/products")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_products_returns_active_only(client: AsyncClient, db_session: AsyncSession):
    db_session.add(Product(
        slug="ai-glasses", category="glasses", name="AI眼镜",
        tagline="实时感知", description="描述", cover_image="/img.jpg", is_active=True,
    ))
    db_session.add(Product(
        slug="hidden", category="toy", name="隐藏产品",
        tagline="测试", description="测试", cover_image="/img.jpg", is_active=False,
    ))
    await db_session.commit()

    response = await client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["slug"] == "ai-glasses"
    assert data[0]["category"] == "glasses"
    assert data[0]["name"] == "AI眼镜"


@pytest.mark.asyncio
async def test_get_product_detail(client: AsyncClient, db_session: AsyncSession):
    product = Product(
        slug="ai-robot", category="robot", name="AI机器人",
        tagline="智能陪伴", description="详细描述", cover_image="/robot.jpg",
    )
    product.features = [ProductFeature(icon="cpu", title="AI处理", description="本地推理", sort_order=0)]
    product.specs    = [ProductSpec(spec_key="重量", spec_value="1.2kg", sort_order=0)]
    product.images   = [ProductImage(image_url="/r1.jpg", alt_text="正面", sort_order=0)]
    db_session.add(product)
    await db_session.commit()

    response = await client.get("/api/v1/products/ai-robot")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "ai-robot"
    assert data["description"] == "详细描述"
    assert len(data["features"]) == 1
    assert data["features"][0]["title"] == "AI处理"
    assert len(data["specs"]) == 1
    assert data["specs"][0]["spec_key"] == "重量"
    assert len(data["images"]) == 1
    assert data["images"][0]["image_url"] == "/r1.jpg"


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    response = await client.get("/api/v1/products/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "产品不存在"


@pytest.mark.asyncio
async def test_get_inactive_product_returns_404(client: AsyncClient, db_session: AsyncSession):
    db_session.add(Product(
        slug="inactive", category="toy", name="下架产品",
        tagline="测试", description="测试", cover_image="/img.jpg", is_active=False,
    ))
    await db_session.commit()

    response = await client.get("/api/v1/products/inactive")
    assert response.status_code == 404
```

- [ ] **Step 2: Run tests — confirm all FAIL**

```bash
pytest tests/test_products.py -v
```

Expected: 5 errors like `ImportError` or `404 not found` — no endpoint exists yet.

- [ ] **Step 3: Create product schemas**

Create `backend/app/models/schemas/product.py`:

```python
from pydantic import BaseModel, ConfigDict
from typing import List


class FeatureOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    icon: str
    title: str
    description: str


class SpecOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    spec_key: str
    spec_value: str


class ImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    image_url: str
    alt_text: str


class ProductListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    slug: str
    category: str
    name: str
    tagline: str
    cover_image: str


class ProductDetailOut(ProductListOut):
    description: str
    features: List[FeatureOut]
    specs: List[SpecOut]
    images: List[ImageOut]


class StatOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    label: str
    value: str
    unit: str
```

- [ ] **Step 4: Create product_crud.py**

Create `backend/app/crud/product_crud.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.domain.product import Product, SiteStat


async def get_active_products(db: AsyncSession) -> list[Product]:
    result = await db.execute(
        select(Product)
        .where(Product.is_active == True)
        .order_by(Product.sort_order)
    )
    return list(result.scalars().all())


async def get_product_by_slug(db: AsyncSession, slug: str) -> Product | None:
    result = await db.execute(
        select(Product)
        .where(Product.slug == slug, Product.is_active == True)
        .options(
            selectinload(Product.features),
            selectinload(Product.specs),
            selectinload(Product.images),
        )
    )
    return result.scalar_one_or_none()


async def get_active_stats(db: AsyncSession) -> list[SiteStat]:
    result = await db.execute(
        select(SiteStat)
        .where(SiteStat.is_active == True)
        .order_by(SiteStat.sort_order)
    )
    return list(result.scalars().all())
```

- [ ] **Step 5: Create products endpoint**

Create `backend/app/api/v1/endpoints/products.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db
from app.crud.product_crud import get_active_products, get_product_by_slug
from app.models.schemas.product import ProductListOut, ProductDetailOut

router = APIRouter()


@router.get("", response_model=List[ProductListOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await get_active_products(db)


@router.get("/{slug}", response_model=ProductDetailOut)
async def get_product(slug: str, db: AsyncSession = Depends(get_db)):
    product = await get_product_by_slug(db, slug)
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product
```

- [ ] **Step 6: Register router in api/v1/__init__.py**

Replace `backend/app/api/v1/__init__.py` with:

```python
from fastapi import APIRouter
from app.api.v1.endpoints import products

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
```

- [ ] **Step 7: Run tests — confirm all PASS**

```bash
pytest tests/test_products.py -v
```

Expected:
```
PASSED tests/test_products.py::test_list_products_empty
PASSED tests/test_products.py::test_list_products_returns_active_only
PASSED tests/test_products.py::test_get_product_detail
PASSED tests/test_products.py::test_get_product_not_found
PASSED tests/test_products.py::test_get_inactive_product_returns_404
5 passed
```

- [ ] **Step 8: Commit**

```bash
git add backend/app/models/schemas/product.py backend/app/crud/product_crud.py backend/app/api/v1/endpoints/products.py backend/app/api/v1/__init__.py backend/tests/test_products.py
git commit -m "feat: add products endpoint with TDD (list + detail)"
```

---

## Task 9: [TDD] Contact Endpoint

**Files:**
- Create: `backend/tests/test_contact.py`
- Create: `backend/app/models/schemas/contact.py`
- Create: `backend/app/crud/contact_crud.py`
- Create: `backend/app/api/v1/endpoints/contact.py`
- Modify: `backend/app/api/v1/__init__.py`

- [ ] **Step 1: Write failing tests**

Create `backend/tests/test_contact.py`:

```python
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_submit_contact_success(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "张三",
        "email": "zhangsan@example.com",
        "inquiry_type": "cooperation",
        "message": "希望与贵公司探讨合作机会",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "24小时" in data["message"]


@pytest.mark.asyncio
async def test_submit_contact_default_inquiry_type(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "李四",
        "email": "lisi@example.com",
        "message": "有问题想咨询",
    })
    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.asyncio
async def test_submit_contact_empty_name(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "   ",
        "email": "test@example.com",
        "message": "留言内容",
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_contact_invalid_email(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "张三",
        "email": "not-an-email",
        "message": "留言内容",
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_contact_empty_message(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "张三",
        "email": "test@example.com",
        "message": "   ",
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_contact_message_too_long(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "张三",
        "email": "test@example.com",
        "message": "x" * 2001,
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_contact_name_too_long(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "张" * 101,
        "email": "test@example.com",
        "message": "留言内容",
    })
    assert response.status_code == 422
```

- [ ] **Step 2: Run tests — confirm all FAIL**

```bash
pytest tests/test_contact.py -v
```

Expected: all 7 tests FAIL (endpoint not found / 404).

- [ ] **Step 3: Create contact schemas**

Create `backend/app/models/schemas/contact.py`:

```python
from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal


class ContactIn(BaseModel):
    name: str
    email: EmailStr
    company: str = ""
    inquiry_type: Literal["cooperation", "media", "other"] = "other"
    message: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("姓名不能为空")
        if len(v) > 100:
            raise ValueError("姓名不能超过100个字符")
        return v

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("留言内容不能为空")
        if len(v) > 2000:
            raise ValueError("留言内容不能超过2000个字符")
        return v


class ContactOut(BaseModel):
    success: bool
    message: str
```

- [ ] **Step 4: Create contact_crud.py**

Create `backend/app/crud/contact_crud.py`:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.domain.contact import ContactSubmission
from app.models.schemas.contact import ContactIn


async def create_contact_submission(
    db: AsyncSession,
    payload: ContactIn,
    ip_address: str | None,
) -> ContactSubmission:
    submission = ContactSubmission(
        name=payload.name,
        email=payload.email,
        company=payload.company,
        inquiry_type=payload.inquiry_type,
        message=payload.message,
        ip_address=ip_address,
    )
    db.add(submission)
    await db.commit()
    return submission
```

- [ ] **Step 5: Create contact endpoint**

Create `backend/app/api/v1/endpoints/contact.py`:

```python
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.crud.contact_crud import create_contact_submission
from app.models.schemas.contact import ContactIn, ContactOut

router = APIRouter()


@router.post("", response_model=ContactOut)
async def submit_contact(
    payload: ContactIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    ip_address = request.client.host if request.client else None
    await create_contact_submission(db, payload, ip_address)
    return ContactOut(success=True, message="提交成功，我们将在24小时内与您联系")
```

- [ ] **Step 6: Register contact router in api/v1/__init__.py**

Replace `backend/app/api/v1/__init__.py` with:

```python
from fastapi import APIRouter
from app.api.v1.endpoints import products, contact

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
```

- [ ] **Step 7: Run tests — confirm all PASS**

```bash
pytest tests/test_contact.py -v
```

Expected:
```
PASSED tests/test_contact.py::test_submit_contact_success
PASSED tests/test_contact.py::test_submit_contact_default_inquiry_type
PASSED tests/test_contact.py::test_submit_contact_empty_name
PASSED tests/test_contact.py::test_submit_contact_invalid_email
PASSED tests/test_contact.py::test_submit_contact_empty_message
PASSED tests/test_contact.py::test_submit_contact_message_too_long
PASSED tests/test_contact.py::test_submit_contact_name_too_long
7 passed
```

- [ ] **Step 8: Commit**

```bash
git add backend/app/models/schemas/contact.py backend/app/crud/contact_crud.py backend/app/api/v1/endpoints/contact.py backend/app/api/v1/__init__.py backend/tests/test_contact.py
git commit -m "feat: add contact form endpoint with validation and TDD"
```

---

## Task 10: [TDD] Stats Endpoint

**Files:**
- Create: `backend/tests/test_stats.py`
- Create: `backend/app/api/v1/endpoints/stats.py`
- Modify: `backend/app/api/v1/__init__.py`

- [ ] **Step 1: Write failing tests**

Create `backend/tests/test_stats.py`:

```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain.product import SiteStat


@pytest.mark.asyncio
async def test_get_stats_empty(client: AsyncClient):
    response = await client.get("/api/v1/stats")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_stats_returns_active_only(client: AsyncClient, db_session: AsyncSession):
    db_session.add(SiteStat(label="专利数量", value="200+", unit="项", sort_order=0, is_active=True))
    db_session.add(SiteStat(label="隐藏数据", value="999", unit="个", sort_order=1, is_active=False))
    await db_session.commit()

    response = await client.get("/api/v1/stats")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["label"] == "专利数量"
    assert data[0]["value"] == "200+"
    assert data[0]["unit"] == "项"


@pytest.mark.asyncio
async def test_get_stats_ordered_by_sort_order(client: AsyncClient, db_session: AsyncSession):
    db_session.add(SiteStat(label="B指标", value="200", unit="个", sort_order=2, is_active=True))
    db_session.add(SiteStat(label="A指标", value="100", unit="项", sort_order=1, is_active=True))
    await db_session.commit()

    response = await client.get("/api/v1/stats")
    data = response.json()
    assert data[0]["label"] == "A指标"
    assert data[1]["label"] == "B指标"
```

- [ ] **Step 2: Run tests — confirm all FAIL**

```bash
pytest tests/test_stats.py -v
```

Expected: 3 tests FAIL.

- [ ] **Step 3: Create stats endpoint**

Create `backend/app/api/v1/endpoints/stats.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db
from app.crud.product_crud import get_active_stats
from app.models.schemas.product import StatOut

router = APIRouter()


@router.get("", response_model=List[StatOut])
async def get_stats(db: AsyncSession = Depends(get_db)):
    return await get_active_stats(db)
```

- [ ] **Step 4: Register stats router in api/v1/__init__.py**

Replace `backend/app/api/v1/__init__.py` with:

```python
from fastapi import APIRouter
from app.api.v1.endpoints import products, contact, stats

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(contact.router,  prefix="/contact",  tags=["contact"])
api_router.include_router(stats.router,    prefix="/stats",    tags=["stats"])
```

- [ ] **Step 5: Run all tests — confirm all pass**

```bash
pytest tests/ -v
```

Expected:
```
15 passed
```

(5 product + 7 contact + 3 stats)

- [ ] **Step 6: Commit**

```bash
git add backend/app/api/v1/endpoints/stats.py backend/app/api/v1/__init__.py backend/tests/test_stats.py
git commit -m "feat: add stats endpoint with TDD — all 15 tests pass"
```

---

## Task 11: Seed Data Script

**Files:**
- Create: `backend/scripts/seed_data.py`

- [ ] **Step 1: Create seed_data.py**

Create `backend/scripts/seed_data.py`:

```python
"""
Seed initial product and stats data.
Run from backend/ directory:
    conda activate ai-full-stack
    python -m scripts.seed_data
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
from app.models.domain.product import (
    Product, ProductFeature, ProductSpec, ProductImage, SiteStat
)


async def seed(session: AsyncSession) -> None:
    # ── Site Stats ──────────────────────────────────────────
    stats = [
        SiteStat(label="核心专利", value="200+", unit="项",  sort_order=0),
        SiteStat(label="研发工程师", value="50+", unit="人", sort_order=1),
        SiteStat(label="合作伙伴", value="30+",  unit="家", sort_order=2),
    ]
    session.add_all(stats)

    # ── AI眼镜 ───────────────────────────────────────────────
    glasses = Product(
        slug="ai-glasses",
        category="glasses",
        name="AI眼镜",
        tagline="实时感知，智能随行",
        description="融合毫米波雷达与边缘计算的新一代AR智能眼镜，实现环境实时感知与信息叠加显示。",
        cover_image="/static/products/glasses-cover.webp",
        sort_order=0,
    )
    glasses.features = [
        ProductFeature(icon="eye",    title="AR叠加显示",  description="低延迟透视显示，信息无缝融入现实", sort_order=0),
        ProductFeature(icon="cpu",    title="端侧AI推理",  description="NPU本地运行，保护数据隐私",         sort_order=1),
        ProductFeature(icon="signal", title="毫米波感知",  description="精准识别距离与姿态",               sort_order=2),
    ]
    glasses.specs = [
        ProductSpec(spec_key="重量",     spec_value="42g",         sort_order=0),
        ProductSpec(spec_key="续航",     spec_value="8小时",       sort_order=1),
        ProductSpec(spec_key="显示",     spec_value="1080p双目",   sort_order=2),
        ProductSpec(spec_key="处理器",   spec_value="自研NPU",     sort_order=3),
        ProductSpec(spec_key="连接",     spec_value="BT5.3 / WiFi 6", sort_order=4),
    ]
    glasses.images = [
        ProductImage(image_url="/static/products/glasses-1.webp", alt_text="AI眼镜正面",   sort_order=0),
        ProductImage(image_url="/static/products/glasses-2.webp", alt_text="AI眼镜侧面",   sort_order=1),
    ]
    session.add(glasses)

    # ── AI机器人 ─────────────────────────────────────────────
    robot = Product(
        slug="ai-robot",
        category="robot",
        name="AI机器人",
        tagline="智能陪伴，情感连接",
        description="搭载大语言模型的家用智能陪伴机器人，具备多模态理解与自然对话能力。",
        cover_image="/static/products/robot-cover.webp",
        sort_order=1,
    )
    robot.features = [
        ProductFeature(icon="brain",  title="LLM对话",    description="自然语言理解，上下文记忆",     sort_order=0),
        ProductFeature(icon="camera", title="视觉感知",    description="人脸识别与情绪分析",           sort_order=1),
        ProductFeature(icon="move",   title="自主移动",    description="激光SLAM导航，避障巡逻",       sort_order=2),
    ]
    robot.specs = [
        ProductSpec(spec_key="身高",     spec_value="35cm",         sort_order=0),
        ProductSpec(spec_key="续航",     spec_value="6小时",        sort_order=1),
        ProductSpec(spec_key="处理器",   spec_value="骁龙8 Gen2",   sort_order=2),
        ProductSpec(spec_key="传感器",   spec_value="ToF+RGB双摄",  sort_order=3),
    ]
    robot.images = [
        ProductImage(image_url="/static/products/robot-1.webp", alt_text="AI机器人正面", sort_order=0),
    ]
    session.add(robot)

    # ── AI玩具 ──────────────────────────────────────────────
    toy = Product(
        slug="ai-toy",
        category="toy",
        name="AI玩具",
        tagline="启蒙智慧，伴随成长",
        description="面向3-12岁儿童的AI教育玩具，通过互动故事与益智游戏激发创造力。",
        cover_image="/static/products/toy-cover.webp",
        sort_order=2,
    )
    toy.features = [
        ProductFeature(icon="book",  title="自适应课程",  description="根据孩子水平动态调整内容", sort_order=0),
        ProductFeature(icon="mic",   title="语音交互",    description="中英双语，自然对话",       sort_order=1),
        ProductFeature(icon="safe",  title="儿童安全",    description="无蓝光屏幕，离线优先",     sort_order=2),
    ]
    toy.specs = [
        ProductSpec(spec_key="适龄",   spec_value="3-12岁",  sort_order=0),
        ProductSpec(spec_key="续航",   spec_value="10小时",  sort_order=1),
        ProductSpec(spec_key="存储",   spec_value="16GB",    sort_order=2),
    ]
    toy.images = [
        ProductImage(image_url="/static/products/toy-1.webp", alt_text="AI玩具正面", sort_order=0),
    ]
    session.add(toy)

    await session.commit()
    print("✓ Seed data inserted: 3 products, 3 site stats")


async def main() -> None:
    engine = create_async_engine(settings.DATABASE_URL)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        await seed(session)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] **Step 2: Run seed script**

```bash
cd d:/Code/python/ai-native-full-stack/backend
python -m scripts.seed_data
```

Expected: `✓ Seed data inserted: 3 products, 3 site stats`

- [ ] **Step 3: Verify via API**

```bash
uvicorn app.main:app --port 8000 &
sleep 2
curl http://localhost:8000/api/v1/products | python -m json.tool
```

Expected: JSON array with 3 products (ai-glasses, ai-robot, ai-toy).

Kill the server: `kill %1` (or `taskkill /f /im uvicorn.exe` on Windows)

- [ ] **Step 4: Run full test suite (seed must not break tests)**

```bash
pytest tests/ -v
```

Expected: 15 passed

- [ ] **Step 5: Commit**

```bash
git add backend/scripts/seed_data.py
git commit -m "feat: add seed data script with 3 products and site stats"
```

---

## Task 12: Frontend Integration Fix

**Files:**
- Modify: `frontend/vite.config.ts` (proxy port 8080 → 8000)

> **Note:** The frontend is already fully implemented. This task only fixes the API proxy target.

- [ ] **Step 1: Fix vite.config.ts proxy port**

In `frontend/vite.config.ts`, change:

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8080',   // ← wrong
```

To:

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',   // ← correct
```

- [ ] **Step 2: Start backend**

```bash
cd d:/Code/python/ai-native-full-stack/backend
conda activate ai-full-stack
uvicorn app.main:app --reload --port 8000
```

- [ ] **Step 3: Start frontend (new terminal)**

```bash
cd d:/Code/python/ai-native-full-stack/frontend
npm run dev
```

Expected: `http://localhost:5173`

- [ ] **Step 4: Verify full stack in browser**

Open `http://localhost:5173` and confirm:
- Homepage loads with navigation
- Product cards appear (loaded from `/api/v1/products`)
- Navigating to `/products/ai-glasses` loads product detail
- Contact form at `/contact` submits without error (check Network tab)
- Stats section shows numbers (if wired in a component)

- [ ] **Step 5: Commit**

```bash
cd d:/Code/python/ai-native-full-stack
git add frontend/vite.config.ts
git commit -m "fix: correct API proxy port from 8080 to 8000"
```

---

## Self-Review Checklist

**Spec coverage:**
- [x] FastAPI + SQLAlchemy 2.0 Async — Tasks 3, 4
- [x] aiosqlite driver — Task 1 (pyproject.toml)
- [x] Alembic migrations — Task 5
- [x] `GET /api/v1/products` — Task 8
- [x] `GET /api/v1/products/{slug}` with relations — Task 8
- [x] `POST /api/v1/contact` with validation — Task 9
- [x] `GET /api/v1/stats` — Task 10
- [x] pytest-asyncio + httpx + in-memory SQLite tests — Tasks 7-10
- [x] Seed data script — Task 11
- [x] No Django — confirmed (no django import anywhere)
- [x] conda activate ai-full-stack — mentioned in every task
- [x] Frontend proxy fix — Task 12
- [x] 15 unit tests total (5 products + 7 contact + 3 stats) — Tasks 8-10
- [x] `frontend-design` skill — all frontend work is already done; invoke for any new component additions

**Type consistency check:**
- `get_active_products` → `list[Product]` ✓ matches products endpoint usage
- `get_product_by_slug` → `Product | None` ✓ matches 404 check in endpoint
- `get_active_stats` → `list[SiteStat]` ✓ matches stats endpoint usage
- `ProductDetailOut` inherits `ProductListOut` ✓ consistent across tasks
- `ContactIn.name` validator strips and checks length ✓ test covers both empty and too-long cases
