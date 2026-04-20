# 单元测试报告：AI智能终端企业官网

**文档版本：** 1.0  
**测试日期：** 2026-04-19  
**测试环境：** Python 3.11.15 / pytest 9.0.3 / pytest-asyncio 1.3.0  
**测试框架：** pytest + pytest-asyncio + httpx (ASGITransport)  
**数据库：** 内存 SQLite（`sqlite+aiosqlite:///:memory:`，每用例独立隔离）  
**测试目录：** `backend/tests/`

---

## 一、测试总览

| 指标 | 数值 |
|------|------|
| 测试文件数 | 3 |
| 用例总数 | 15 |
| 通过 | **15** |
| 失败 | 0 |
| 跳过 | 0 |
| 执行时间 | 0.48 s |
| 通过率 | **100%** |

---

## 二、执行日志

```
============================= test session starts =============================
platform win32 -- Python 3.11.15, pytest-9.0.3, pluggy-1.6.0
rootdir: D:\Code\python\ai-native-full-stack\backend
plugins: anyio-4.13.0, asyncio-1.3.0
asyncio: mode=Mode.STRICT

tests/test_contact.py::test_submit_contact_success               PASSED  [  6%]
tests/test_contact.py::test_submit_contact_default_inquiry_type  PASSED  [ 13%]
tests/test_contact.py::test_submit_contact_empty_name            PASSED  [ 20%]
tests/test_contact.py::test_submit_contact_invalid_email         PASSED  [ 26%]
tests/test_contact.py::test_submit_contact_empty_message         PASSED  [ 33%]
tests/test_contact.py::test_submit_contact_message_too_long      PASSED  [ 40%]
tests/test_contact.py::test_submit_contact_name_too_long         PASSED  [ 46%]
tests/test_products.py::test_list_products_empty                 PASSED  [ 53%]
tests/test_products.py::test_list_products_returns_active_only   PASSED  [ 60%]
tests/test_products.py::test_get_product_detail                  PASSED  [ 66%]
tests/test_products.py::test_get_product_not_found               PASSED  [ 73%]
tests/test_products.py::test_get_inactive_product_returns_404    PASSED  [ 80%]
tests/test_stats.py::test_get_stats_empty                        PASSED  [ 86%]
tests/test_stats.py::test_get_stats_returns_active_only          PASSED  [ 93%]
tests/test_stats.py::test_get_stats_ordered_by_sort_order        PASSED  [100%]

============================= 15 passed in 0.48s ==============================
```

---

## 三、用例明细

### 3.1 产品接口测试（test_products.py）

共 **5** 个用例，全部通过。

| # | 用例名称 | 测试方法 | 路径 | 预期状态码 | 核心断言 | 结果 |
|---|---------|---------|------|-----------|---------|------|
| 1 | test_list_products_empty | GET | `/api/v1/products` | 200 | 空数据库返回 `[]` | ✅ PASS |
| 2 | test_list_products_returns_active_only | GET | `/api/v1/products` | 200 | 仅返回 `is_active=True` 的产品，过滤下架产品 | ✅ PASS |
| 3 | test_get_product_detail | GET | `/api/v1/products/ai-robot` | 200 | 返回完整产品含 features/specs/images 关联数据 | ✅ PASS |
| 4 | test_get_product_not_found | GET | `/api/v1/products/nonexistent` | 404 | `detail == "产品不存在"` | ✅ PASS |
| 5 | test_get_inactive_product_returns_404 | GET | `/api/v1/products/inactive` | 404 | 下架产品视为不存在，返回 404 | ✅ PASS |

**关键测试逻辑（test_get_product_detail）：**

```python
product = Product(slug="ai-robot", category="robot", name="AI机器人", ...)
product.features = [ProductFeature(icon="cpu", title="AI处理", description="本地推理")]
product.specs    = [ProductSpec(spec_key="重量", spec_value="1.2kg")]
product.images   = [ProductImage(image_url="/r1.jpg", alt_text="正面")]
db_session.add(product)
await db_session.commit()

response = await client.get("/api/v1/products/ai-robot")
assert response.status_code == 200
data = response.json()
assert len(data["features"]) == 1
assert data["features"][0]["title"] == "AI处理"
assert len(data["specs"]) == 1
assert len(data["images"]) == 1
```

---

### 3.2 联系表单测试（test_contact.py）

共 **7** 个用例，全部通过。

| # | 用例名称 | 方法 | 路径 | 预期状态码 | 核心断言 | 结果 |
|---|---------|------|------|-----------|---------|------|
| 1 | test_submit_contact_success | POST | `/api/v1/contact` | 200 | `success=True`，`message` 含"24小时" | ✅ PASS |
| 2 | test_submit_contact_default_inquiry_type | POST | `/api/v1/contact` | 200 | 不传 `inquiry_type` 时默认值生效，提交成功 | ✅ PASS |
| 3 | test_submit_contact_empty_name | POST | `/api/v1/contact` | 422 | 空白姓名（全空格）被校验拦截 | ✅ PASS |
| 4 | test_submit_contact_invalid_email | POST | `/api/v1/contact` | 422 | 非法邮箱格式被 EmailStr 拦截 | ✅ PASS |
| 5 | test_submit_contact_empty_message | POST | `/api/v1/contact` | 422 | 空白留言（全空格）被校验拦截 | ✅ PASS |
| 6 | test_submit_contact_message_too_long | POST | `/api/v1/contact` | 422 | 留言超 2000 字符被拦截 | ✅ PASS |
| 7 | test_submit_contact_name_too_long | POST | `/api/v1/contact` | 422 | 姓名超 100 字符被拦截 | ✅ PASS |

**关键测试逻辑（边界校验）：**

```python
# 超长留言：2001 字符
await client.post("/api/v1/contact", json={
    "name": "张三", "email": "test@example.com", "message": "x" * 2001
})  # → 422

# 超长姓名：101 个汉字
await client.post("/api/v1/contact", json={
    "name": "张" * 101, "email": "test@example.com", "message": "留言内容"
})  # → 422
```

---

### 3.3 站点统计测试（test_stats.py）

共 **3** 个用例，全部通过。

| # | 用例名称 | 方法 | 路径 | 预期状态码 | 核心断言 | 结果 |
|---|---------|------|------|-----------|---------|------|
| 1 | test_get_stats_empty | GET | `/api/v1/stats` | 200 | 空数据库返回 `[]` | ✅ PASS |
| 2 | test_get_stats_returns_active_only | GET | `/api/v1/stats` | 200 | 仅返回 `is_active=True` 的统计项，过滤隐藏数据 | ✅ PASS |
| 3 | test_get_stats_ordered_by_sort_order | GET | `/api/v1/stats` | 200 | 按 `sort_order` 升序排列 | ✅ PASS |

**关键测试逻辑（排序验证）：**

```python
db_session.add(SiteStat(label="B指标", value="200", sort_order=2))
db_session.add(SiteStat(label="A指标", value="100", sort_order=1))
await db_session.commit()

response = await client.get("/api/v1/stats")
data = response.json()
assert data[0]["label"] == "A指标"   # sort_order=1 在前
assert data[1]["label"] == "B指标"   # sort_order=2 在后
```

---

## 四、测试架构说明

### 4.1 Fixture 设计

```python
# backend/tests/conftest.py

@pytest_asyncio.fixture
async def db_session():
    """每个测试用例独立的内存 SQLite，自动建表/销毁"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def client(db_session):
    """覆盖 get_db 依赖，注入测试数据库"""
    app.dependency_overrides[get_db] = lambda: (yield db_session)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
```

**隔离机制：**
- 每个测试函数拥有独立的内存数据库实例
- 测试结束后自动 `drop_all`，无数据污染
- 通过 `dependency_overrides` 替换生产数据库依赖，不依赖外部服务

### 4.2 异步配置

```toml
# backend/pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

所有测试用例均为 `async def`，通过 pytest-asyncio 自动运行。

---

## 五、覆盖接口汇总

| 接口 | 方法 | 覆盖用例数 | 覆盖场景 |
|------|------|----------|---------|
| `/api/v1/products` | GET | 2 | 空列表、活跃过滤 |
| `/api/v1/products/{slug}` | GET | 3 | 详情完整性、404不存在、404下架 |
| `/api/v1/contact` | POST | 7 | 正常提交、默认字段、5种异常输入 |
| `/api/v1/stats` | GET | 3 | 空列表、活跃过滤、排序 |

---

## 六、已知限制

| 项目 | 说明 |
|------|------|
| 数据库类型差异 | 测试使用内存 SQLite，生产同为 SQLite，无差异风险 |
| IP 地址记录 | 单元测试中 `request.client` 为模拟值，未验证 IP 记录逻辑 |
| 并发场景 | 未覆盖高并发写入场景 |
| 数据持久化 | 测试不验证数据库持久化，仅验证 HTTP 响应 |
