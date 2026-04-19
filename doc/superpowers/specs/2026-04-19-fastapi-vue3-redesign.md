# Design Spec: FastAPI + Vue3 重构方案

**日期：** 2026-04-19  
**状态：** 待实施  
**关联文档：** doc/TechSpec-AI智能终端企业官网-V2.0.md

---

## 背景与目标

将原有 FastAPI + Django ORM hybrid 架构简化为纯 FastAPI + SQLAlchemy 2.0 Async 方案，移除 Django 框架依赖，统一技术栈，降低维护复杂度。

---

## 关键决策

| 决策项 | 选择 | 原因 |
|--------|------|------|
| ORM | SQLAlchemy 2.0 Async + Alembic | 原生 async，完整迁移能力 |
| 数据库 | SQLite + aiosqlite | 轻量本地，早期部署足够 |
| Admin UI | 无 | 暂不需要，后续按需补充 |
| 依赖管理 | pyproject.toml | 现代 Python 标准，替代 requirements.txt |
| 测试框架 | pytest-asyncio + httpx | 内存 SQLite 隔离，AsyncClient 测试 endpoint |

---

## 架构

```
Client Browser
    │ HTTPS
Nginx (反向代理)
    ├── /        → Vue3 静态资源
    └── /api/    → FastAPI :8000
                      │
                 SQLAlchemy 2.0 Async
                      │
                 SQLite (aiosqlite)
```

---

## 后端目录结构

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── products.py
│   │   │   │   ├── contact.py
│   │   │   │   └── stats.py
│   │   │   └── __init__.py
│   │   └── deps.py
│   ├── core/
│   │   └── config.py
│   ├── crud/
│   │   ├── product_crud.py
│   │   └── contact_crud.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── domain/
│   │   │   ├── product.py
│   │   │   └── contact.py
│   │   └── schemas/
│   │       ├── product.py
│   │       └── contact.py
│   └── main.py
├── alembic/
├── alembic.ini
├── scripts/
├── tests/
│   ├── conftest.py
│   ├── test_products.py
│   ├── test_contact.py
│   └── test_stats.py
├── .env
├── pyproject.toml
└── Dockerfile
```

---

## 数据模型

### Product 相关（4张表）

- `products` — Product 主表
- `product_features` — 功能特性（1:N）
- `product_specs` — 规格参数（1:N）
- `product_images` — 产品图片（1:N）
- `site_stats` — 首页统计数字

### Contact（1张表）

- `contact_submissions` — 联系表单提交记录

---

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/products` | 产品列表 |
| GET | `/api/v1/products/{slug}` | 产品详情 |
| GET | `/api/v1/stats` | 站点统计数字 |
| POST | `/api/v1/contact` | 提交联系表单 |

---

## 单元测试策略

- **框架：** pytest + pytest-asyncio + httpx
- **数据库：** `sqlite+aiosqlite:///:memory:` 内存库，每次测试独立
- **覆盖范围：**
  - CRUD 层：增删改查逻辑
  - API endpoint：请求/响应格式、错误码
  - Schema 验证：ContactIn 字段校验（空值、长度限制）

---

## 依赖

```toml
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

## 开发启动

```bash
conda activate ai-full-stack
cd backend
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
