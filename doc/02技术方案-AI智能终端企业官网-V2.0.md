# 技术方案：AI智能终端企业官网 V2.0

**文档版本：** 2.0  
**日期：** 2026-04-19  
**关联PRD：** PRD-AI智能终端企业官网-V1.0.md  
**技术栈：** Vue3 + FastAPI + SQLAlchemy + SQLite  
**变更说明：** 移除 Django 框架，采用纯 FastAPI + SQLAlchemy 2.0 Async 方案

---

## 一、整体架构

### 1.1 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                      Client Browser                     │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────┐
│                    Nginx (反向代理)                       │
│          /          →  Vue3 静态资源                     │
│          /api/      →  FastAPI :8000                    │
└──────┬──────────────────────────────────────────────────┘
       │
┌──────▼──────────┐         ┌──────────────────────────┐
│   Vue3 前端     │         │   FastAPI 服务            │
│   (Vite构建)    │         │   (uvicorn运行)           │
│                 │         │                          │
│  Vue Router 4   │         │  SQLAlchemy 2.0 Async    │
│  Pinia Store    │         │  Alembic 迁移管理        │
│  Tailwind CSS   │         │  Pydantic 数据校验       │
│  GSAP 动效      │         └──────────┬───────────────┘
└─────────────────┘                    │
                            ┌──────────▼───────────────┐
                            │   SQLite (aiosqlite)     │
                            │   db.sqlite3             │
                            └──────────────────────────┘
```

### 1.2 技术栈选型

| 层级 | 技术 | 版本 | 职责 |
|------|------|------|------|
| 前端框架 | Vue3 | 3.4+ | SPA页面渲染、路由、状态管理 |
| 前端构建 | Vite | 5.x | 开发服务器、生产打包 |
| 前端路由 | Vue Router | 4.x | 客户端路由 |
| 前端状态 | Pinia | 2.x | 全局状态管理 |
| 前端样式 | Tailwind CSS | 3.x | 原子化CSS |
| 前端动效 | GSAP | 3.x | 滚动动效、数字计数、Hero动画 |
| HTTP客户端 | Axios | 1.x | API请求封装 |
| API框架 | FastAPI | 0.115+ | REST API、自动文档 |
| ORM | SQLAlchemy | 2.0+ | 异步ORM，Mapped 风格模型定义 |
| 迁移工具 | Alembic | 1.13+ | 数据库版本管理 |
| 数据库驱动 | aiosqlite | 0.20+ | SQLite 异步驱动 |
| 数据库 | SQLite | 3.x | 本地轻量级持久化 |
| ASGI服务器 | Uvicorn | 0.30+ | FastAPI生产运行 |
| 反向代理 | Nginx | 1.24+ | 静态资源服务、API代理 |

---

## 二、项目结构

```
ai-native-full-stack/
├── doc/                          # 文档目录
│   ├── PRD-AI智能终端企业官网-V1.0.md
│   ├── TechSpec-AI智能终端企业官网-V1.0.md  # 旧版（归档）
│   └── TechSpec-AI智能终端企业官网-V2.0.md  # 当前版本
│
├── frontend/                     # Vue3 前端（结构同 V1）
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── AppNav.vue
│   │   │   │   ├── AppFooter.vue
│   │   │   │   └── AppBtn.vue
│   │   │   ├── home/
│   │   │   │   ├── HeroSection.vue
│   │   │   │   ├── ProductMatrix.vue
│   │   │   │   ├── TechHighlights.vue
│   │   │   │   ├── BrandStatement.vue
│   │   │   │   ├── MediaBadges.vue
│   │   │   │   └── CtaSection.vue
│   │   │   └── product/
│   │   │       ├── ProductHero.vue
│   │   │       ├── ProductFeatures.vue
│   │   │       ├── ProductSpecs.vue
│   │   │       ├── ProductScenes.vue
│   │   │       └── ProductGallery.vue
│   │   ├── views/
│   │   │   ├── HomeView.vue
│   │   │   ├── ProductView.vue
│   │   │   ├── AboutView.vue
│   │   │   └── ContactView.vue
│   │   ├── router/index.ts
│   │   ├── stores/
│   │   │   ├── product.ts
│   │   │   └── contact.ts
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   ├── products.ts
│   │   │   └── contact.ts
│   │   ├── types/index.ts
│   │   ├── composables/
│   │   │   ├── useScrollAnimation.ts
│   │   │   └── useCountUp.ts
│   │   ├── App.vue
│   │   └── main.ts
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   └── package.json
│
├── backend/                      # Python 后端
│   ├── app/                      # 应用主模块
│   │   ├── api/                  # 接口层
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── products.py
│   │   │   │   │   ├── contact.py
│   │   │   │   │   └── stats.py
│   │   │   │   └── __init__.py
│   │   │   └── deps.py           # 依赖注入 (DB Session)
│   │   ├── core/                 # 核心配置
│   │   │   └── config.py         # pydantic-settings 配置类
│   │   ├── crud/                 # 数据库增删改查
│   │   │   ├── product_crud.py
│   │   │   └── contact_crud.py
│   │   ├── db/                   # 数据库相关
│   │   │   ├── base.py           # SQLAlchemy DeclarativeBase
│   │   │   └── session.py        # AsyncSession 工厂
│   │   ├── models/               # 模型定义
│   │   │   ├── domain/           # SQLAlchemy ORM 模型
│   │   │   │   ├── product.py    # Product/Feature/Spec/Image/SiteStat
│   │   │   │   └── contact.py    # ContactSubmission
│   │   │   └── schemas/          # Pydantic 请求/响应结构
│   │   │       ├── product.py
│   │   │       └── contact.py
│   │   └── main.py               # FastAPI 入口
│   ├── alembic/                  # 数据库迁移文件
│   ├── alembic.ini
│   ├── scripts/                  # 运维脚本 (seed数据等)
│   ├── tests/                    # 单元测试
│   │   ├── conftest.py
│   │   ├── test_products.py
│   │   ├── test_contact.py
│   │   └── test_stats.py
│   ├── .env
│   ├── pyproject.toml
│   └── Dockerfile
│
├── nginx/
│   └── nginx.conf
└── .env.example
```

---

## 三、数据库设计

### 3.1 SQLAlchemy 模型

```python
# backend/app/models/domain/product.py
from sqlalchemy import String, Text, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id          : Mapped[int]  = mapped_column(primary_key=True, autoincrement=True)
    slug        : Mapped[str]  = mapped_column(String(50), unique=True, index=True)
    category    : Mapped[str]  = mapped_column(String(20))   # glasses/robot/toy
    name        : Mapped[str]  = mapped_column(String(100))
    tagline     : Mapped[str]  = mapped_column(String(200))
    description : Mapped[str]  = mapped_column(Text)
    cover_image : Mapped[str]  = mapped_column(String(500))
    is_active   : Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order  : Mapped[int]  = mapped_column(Integer, default=0)
    created_at  : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at  : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow,
                                                   onupdate=datetime.utcnow)

    features : Mapped[list["ProductFeature"]] = relationship(
        back_populates="product", order_by="ProductFeature.sort_order",
        cascade="all, delete-orphan"
    )
    specs    : Mapped[list["ProductSpec"]]    = relationship(
        back_populates="product", order_by="ProductSpec.sort_order",
        cascade="all, delete-orphan"
    )
    images   : Mapped[list["ProductImage"]]   = relationship(
        back_populates="product", order_by="ProductImage.sort_order",
        cascade="all, delete-orphan"
    )


class ProductFeature(Base):
    __tablename__ = "product_features"

    id          : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id  : Mapped[int] = mapped_column(ForeignKey("products.id"))
    icon        : Mapped[str] = mapped_column(String(100))
    title       : Mapped[str] = mapped_column(String(100))
    description : Mapped[str] = mapped_column(String(300))
    sort_order  : Mapped[int] = mapped_column(Integer, default=0)
    product     : Mapped["Product"] = relationship(back_populates="features")


class ProductSpec(Base):
    __tablename__ = "product_specs"

    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    spec_key   : Mapped[str] = mapped_column(String(100))
    spec_value : Mapped[str] = mapped_column(String(200))
    sort_order : Mapped[int] = mapped_column(Integer, default=0)
    product    : Mapped["Product"] = relationship(back_populates="specs")


class ProductImage(Base):
    __tablename__ = "product_images"

    id         : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id : Mapped[int] = mapped_column(ForeignKey("products.id"))
    image_url  : Mapped[str] = mapped_column(String(500))
    alt_text   : Mapped[str] = mapped_column(String(200), default="")
    sort_order : Mapped[int] = mapped_column(Integer, default=0)
    product    : Mapped["Product"] = relationship(back_populates="images")


class SiteStat(Base):
    __tablename__ = "site_stats"

    id         : Mapped[int]  = mapped_column(primary_key=True, autoincrement=True)
    label      : Mapped[str]  = mapped_column(String(100))
    value      : Mapped[str]  = mapped_column(String(50))
    unit       : Mapped[str]  = mapped_column(String(50), default="")
    sort_order : Mapped[int]  = mapped_column(Integer, default=0)
    is_active  : Mapped[bool] = mapped_column(Boolean, default=True)
```

```python
# backend/app/models/domain/contact.py
from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base


class ContactSubmission(Base):
    __tablename__ = "contact_submissions"

    id           : Mapped[int]       = mapped_column(primary_key=True, autoincrement=True)
    name         : Mapped[str]       = mapped_column(String(100))
    email        : Mapped[str]       = mapped_column(String(254))
    company      : Mapped[str]       = mapped_column(String(200), default="")
    inquiry_type : Mapped[str]       = mapped_column(String(20), default="other")
    message      : Mapped[str]       = mapped_column(Text)
    status       : Mapped[str]       = mapped_column(String(20), default="pending")
    ip_address   : Mapped[str | None] = mapped_column(String(45), nullable=True)
    submitted_at : Mapped[datetime]  = mapped_column(DateTime, default=datetime.utcnow)
    updated_at   : Mapped[datetime]  = mapped_column(DateTime, default=datetime.utcnow,
                                                     onupdate=datetime.utcnow)
    notes        : Mapped[str]       = mapped_column(Text, default="")
```

### 3.2 ER 图

```
Product (1) ──< ProductFeature (N)
Product (1) ──< ProductSpec    (N)
Product (1) ──< ProductImage   (N)

ContactSubmission  (独立表)
SiteStat           (独立表)
```

---

## 四、数据库会话管理

```python
# backend/app/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

```python
# backend/app/db/session.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
```

```python
# backend/app/api/deps.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session_factory

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
```

---

## 五、API 设计

### 5.1 接口总览

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| GET | `/api/v1/products` | 获取产品列表 | 无 |
| GET | `/api/v1/products/{slug}` | 获取产品详情 | 无 |
| GET | `/api/v1/stats` | 获取站点统计数字 | 无 |
| POST | `/api/v1/contact` | 提交联系表单 | 无 |

### 5.2 Pydantic Schemas

```python
# backend/app/models/schemas/product.py
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

```python
# backend/app/models/schemas/contact.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal

class ContactIn(BaseModel):
    name: str
    email: EmailStr
    company: str = ""
    inquiry_type: Literal['cooperation', 'media', 'other'] = 'other'
    message: str

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('姓名不能为空')
        if len(v) > 100:
            raise ValueError('姓名不能超过100个字符')
        return v.strip()

    @field_validator('message')
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('留言内容不能为空')
        if len(v) > 2000:
            raise ValueError('留言内容不能超过2000个字符')
        return v.strip()

class ContactOut(BaseModel):
    success: bool
    message: str
```

### 5.3 路由实现

```python
# backend/app/api/v1/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api.deps import get_db
from app.models.domain.product import Product
from app.models.schemas.product import ProductListOut, ProductDetailOut
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[ProductListOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).where(Product.is_active == True).order_by(Product.sort_order)
    )
    return result.scalars().all()

@router.get("/{slug}", response_model=ProductDetailOut)
async def get_product(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product)
        .where(Product.slug == slug, Product.is_active == True)
        .options(
            selectinload(Product.features),
            selectinload(Product.specs),
            selectinload(Product.images),
        )
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product
```

```python
# backend/app/api/v1/endpoints/contact.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.models.domain.contact import ContactSubmission
from app.models.schemas.contact import ContactIn, ContactOut

router = APIRouter(prefix="/contact", tags=["contact"])

@router.post("", response_model=ContactOut)
async def submit_contact(
    payload: ContactIn,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    submission = ContactSubmission(
        name=payload.name,
        email=payload.email,
        company=payload.company,
        inquiry_type=payload.inquiry_type,
        message=payload.message,
        ip_address=request.client.host if request.client else None,
    )
    db.add(submission)
    await db.commit()
    return ContactOut(success=True, message="提交成功，我们将在24小时内与您联系")
```

```python
# backend/app/api/v1/endpoints/stats.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db
from app.models.domain.product import SiteStat
from app.models.schemas.product import StatOut
from typing import List

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("", response_model=List[StatOut])
async def get_stats(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SiteStat).where(SiteStat.is_active == True).order_by(SiteStat.sort_order)
    )
    return result.scalars().all()
```

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints.products import router as products_router
from app.api.v1.endpoints.contact import router as contact_router
from app.api.v1.endpoints.stats import router as stats_router

app = FastAPI(
    title="AI智能终端官网 API",
    version="2.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(products_router, prefix="/api/v1")
app.include_router(contact_router,  prefix="/api/v1")
app.include_router(stats_router,    prefix="/api/v1")
```

### 5.4 响应格式（同 V1）

```json
// GET /api/v1/products
[
  {
    "slug": "ai-glasses",
    "category": "glasses",
    "name": "AI眼镜",
    "tagline": "实时感知，智能随行",
    "cover_image": "/static/products/glasses-cover.webp"
  }
]
```

---

## 六、配置管理

```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"
    DATABASE_URL: str = "sqlite+aiosqlite:///./db.sqlite3"
    ALLOWED_HOSTS: List[str] = ["localhost"]
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    model_config = {"env_file": ".env"}

settings = Settings()
```

```bash
# backend/.env.example
DEBUG=true
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3
CORS_ORIGINS=http://localhost:5173
```

---

## 七、单元测试

### 7.1 测试策略

- 框架：**pytest + pytest-asyncio + httpx**
- 数据库：每个测试函数使用独立内存 SQLite（`sqlite+aiosqlite:///:memory:`）
- 通过 `conftest.py` fixture 自动创建/销毁表结构

### 7.2 conftest.py

```python
# backend/tests/conftest.py
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.db.base import Base
from app.main import app
from app.api.deps import get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
```

### 7.3 测试覆盖范围

```python
# test_products.py — 覆盖项
# - GET /api/v1/products 返回空列表
# - GET /api/v1/products 返回活跃产品列表
# - GET /api/v1/products/{slug} 返回产品详情
# - GET /api/v1/products/{slug} 不存在时返回 404

# test_contact.py — 覆盖项
# - POST /api/v1/contact 正常提交返回 success=true
# - POST /api/v1/contact 空姓名返回 422
# - POST /api/v1/contact 无效邮箱返回 422
# - POST /api/v1/contact 空留言返回 422

# test_stats.py — 覆盖项
# - GET /api/v1/stats 返回空列表
# - GET /api/v1/stats 只返回 is_active=True 的数据
```

---

## 八、依赖清单

```toml
# backend/pyproject.toml
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
```

---

## 九、前端设计（同 V1，无变更）

### 9.1 路由配置

```typescript
// frontend/src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: 'AI智能终端 — 智能，从此触手可及' }
  },
  {
    path: '/products/:slug',
    name: 'product',
    component: () => import('@/views/ProductView.vue'),
    meta: { title: '产品详情' }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/AboutView.vue'),
    meta: { title: '关于我们' }
  },
  {
    path: '/contact',
    name: 'contact',
    component: () => import('@/views/ContactView.vue'),
    meta: { title: '联系我们' }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0, behavior: 'smooth' })
})

router.beforeEach((to) => {
  document.title = to.meta.title as string ?? 'AI智能终端'
})

export default router
```

### 9.2 Tailwind 设计系统

```typescript
// frontend/tailwind.config.ts
export default {
  content: ['./index.html', './src/**/*.{vue,ts}'],
  theme: {
    extend: {
      colors: {
        bg:     { primary: '#0A0A0F', secondary: '#111827' },
        accent: { cyan: '#00F5FF', purple: '#7C3AED' },
        text:   { primary: '#F9FAFB', secondary: '#9CA3AF' },
        border: { base: '#1F2937' },
      },
      fontFamily: {
        sans: ['Inter', 'PingFang SC', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'glow-cyan':   '0 0 20px rgba(0, 245, 255, 0.3)',
        'glow-purple': '0 0 20px rgba(124, 58, 237, 0.3)',
      },
      backgroundImage: {
        'gradient-brand': 'linear-gradient(135deg, #00F5FF 0%, #7C3AED 100%)',
      },
    }
  },
}
```

### 9.3 Vite 代理配置

```typescript
// frontend/vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: { alias: { '@': path.resolve(__dirname, 'src') } },
  server: {
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true }
    }
  }
})
```

---

## 十、开发环境启动

### 10.1 后端

```bash
# 激活 conda 环境
conda activate ai-full-stack

# 安装依赖
cd backend
pip install -e ".[dev]"

# 初始化数据库迁移
alembic init alembic
alembic revision --autogenerate -m "init"
alembic upgrade head

# 启动 FastAPI
uvicorn app.main:app --reload --port 8000
```

### 10.2 前端

```bash
cd frontend
npm install
npm run dev        # 开发服务器 http://localhost:5173
npm run build      # 生产构建 → dist/
```

### 10.3 运行测试

```bash
cd backend
pytest tests/ -v
```

---

## 十一、Nginx 生产部署

```nginx
# nginx/nginx.conf
server {
    listen 80;
    server_name yourdomain.com;

    root /var/www/ai-website/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass         http://127.0.0.1:8000;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location ~* \.(js|css|png|jpg|jpeg|webp|svg|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
}
```

---

## 十二、开发里程碑

| 阶段 | 任务 | 产出 |
|------|------|------|
| Week 1 | 环境搭建、数据库初始化（Alembic）、数据录入（seed脚本）、单元测试 | 可用后端API + 全部测试通过 |
| Week 2 | 首页开发（Hero、产品矩阵、技术亮点、CTA） | 首页静态渲染 |
| Week 3 | 产品详情页 × 3、关于我们页 | 完整产品展示 |
| Week 4 | 联系页 + 表单提交 + 动效打磨 + SEO meta | 功能完整版本 |
| Week 5 | 性能优化、跨浏览器测试、Nginx部署、上线 | 生产上线 |

---

**文档状态：** 待技术负责人评审  
**下一步：** 评审通过后，按 Week 1 任务启动项目脚手架搭建
