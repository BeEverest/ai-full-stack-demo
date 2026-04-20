# 系统功能测试报告：AI智能终端企业官网

**文档版本：** 1.0  
**测试日期：** 2026-04-19  
**测试环境：** Python 3.11.15 / FastAPI 0.115+ / uvicorn  
**测试方式：** 真实 HTTP 请求（urllib.request 直连后端服务）  
**后端地址：** `http://localhost:8002`  
**数据库：** SQLite（`backend/db.sqlite3`，含 seed 初始数据）

---

## 一、测试总览

| 指标 | 数值 |
|------|------|
| 测试模块数 | 3（产品、统计、联系表单） |
| 用例总数 | 18 |
| 通过 | **18** |
| 失败 | 0 |
| 通过率 | **100%** |

---

## 二、测试环境说明

### 2.1 初始数据（Seed）

测试前已通过 `python -m scripts.seed_data` 导入：

| 数据类型 | 条数 | 说明 |
|---------|------|------|
| 产品（Product） | 3 | ai-glasses / ai-robot / ai-toy，均为 `is_active=True` |
| 站点统计（SiteStat） | 4 | 自研专利、核心工程师、合作伙伴、用户测试里程 |

### 2.2 后端服务

```bash
conda activate ai-full-stack
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

---

## 三、测试用例明细

### 3.1 产品模块（7 个用例）

#### TC-PRD-01：产品列表正常返回

| 字段 | 内容 |
|------|------|
| 请求 | `GET /api/v1/products` |
| 前置条件 | 数据库已导入 3 条活跃产品 |
| 预期 | HTTP 200，返回 3 条产品的 JSON 数组 |
| 断言 | `len(data) == 3`，含 slug/name/category/tagline/cover_image 字段 |
| **结果** | ✅ **PASS** |

```json
// 响应示例（节选）
[
  {"slug": "ai-glasses", "category": "glasses", "name": "VISION G1", ...},
  {"slug": "ai-robot",   "category": "robot",   "name": "NEXUS R2",  ...},
  {"slug": "ai-toy",     "category": "toy",     "name": "MOCHI A1",  ...}
]
```

---

#### TC-PRD-02：产品列表响应结构校验

| 字段 | 内容 |
|------|------|
| 请求 | `GET /api/v1/products` |
| 预期 | 列表项只包含摘要字段，不含 `description`（详情字段不外泄） |
| 断言 | `"description" not in data[0]`，三个 slug 均符合预期 |
| **结果** | ✅ **PASS** |

---

#### TC-PRD-03：产品详情 — ai-glasses

| 字段 | 内容 |
|------|------|
| 请求 | `GET /api/v1/products/ai-glasses` |
| 预期 | HTTP 200，含完整关联数据 |
| 断言 | `slug == "ai-glasses"`，`features`/`specs`/`images` 均非空数组，含 `description` |
| **结果** | ✅ **PASS** |

---

#### TC-PRD-04：产品详情 — ai-robot

| 字段 | 内容 |
|------|------|
| 请求 | `GET /api/v1/products/ai-robot` |
| 预期 | HTTP 200，含 description 字段 |
| 断言 | `slug == "ai-robot"`，`"description" in data` |
| **结果** | ✅ **PASS** |

---

#### TC-PRD-05：产品详情 — ai-toy

| 字段 | 内容 |
|------|------|
| 请求 | `GET /api/v1/products/ai-toy` |
| 预期 | HTTP 200 |
| 断言 | `slug == "ai-toy"` |
| **结果** | ✅ **PASS** |

---

#### TC-PRD-06：产品详情 — 不存在的 slug

| 字段 | 内容 |
|------|------|
| 请求 | `GET /api/v1/products/not-exist` |
| 预期 | HTTP 404，错误信息为"产品不存在" |
| 断言 | `status == 404`，`data["detail"] == "产品不存在"` |
| **结果** | ✅ **PASS** |

```json
// 响应
{"detail": "产品不存在"}
```

---

#### TC-PRD-07：产品详情 — 404 错误文案验证

| 字段 | 内容 |
|------|------|
| 请求 | `GET /api/v1/products/xxx-yyy` |
| 预期 | HTTP 404，含中文提示 |
| 断言 | `"产品不存在" in str(data)` |
| **结果** | ✅ **PASS** |

---

### 3.2 站点统计模块（2 个用例）

#### TC-STAT-01：统计数据正常返回

| 字段 | 内容 |
|------|------|
| 请求 | `GET /api/v1/stats` |
| 预期 | HTTP 200，返回非空数组 |
| 断言 | `len(data) > 0`，每条含 label/value/unit 字段 |
| **结果** | ✅ **PASS** |

```json
// 响应示例（节选）
[
  {"label": "自研专利",       "value": "60+",    "unit": "项"},
  {"label": "核心工程师",     "value": "80+",    "unit": "人"},
  {"label": "合作伙伴",       "value": "120+",   "unit": "家"},
  {"label": "用户测试里程",   "value": "10万公里", "unit": ""}
]
```

---

#### TC-STAT-02：统计数据字段类型

| 字段 | 内容 |
|------|------|
| 请求 | `GET /api/v1/stats` |
| 预期 | label/value 均为字符串类型 |
| 断言 | `isinstance(s["label"], str) and isinstance(s["value"], str)` 对全部条目成立 |
| **结果** | ✅ **PASS** |

---

### 3.3 联系表单模块（9 个用例）

#### TC-CONTACT-01：正常提交

| 字段 | 内容 |
|------|------|
| 请求 | `POST /api/v1/contact` |
| 请求体 | `{"name":"张三","email":"test@example.com","message":"希望咨询合作"}` |
| 预期 | HTTP 200，`success=true`，含"24小时"提示 |
| 断言 | `data["success"] is True`，`"24小时" in data["message"]` |
| **结果** | ✅ **PASS** |

```json
// 响应
{"success": true, "message": "提交成功，我们将在24小时内与您联系"}
```

---

#### TC-CONTACT-02：含 company 字段提交

| 字段 | 内容 |
|------|------|
| 请求体 | `{"name":"李四","email":"lisi@example.com","company":"测试科技","message":"询价咨询"}` |
| 预期 | HTTP 200，company 为可选字段，提交成功 |
| 断言 | `data["success"] is True` |
| **结果** | ✅ **PASS** |

---

#### TC-CONTACT-03：inquiry_type = media

| 字段 | 内容 |
|------|------|
| 请求体 | `{"name":"王五","email":"wangwu@example.com","inquiry_type":"media","message":"媒体采访申请"}` |
| 预期 | HTTP 200，inquiry_type 枚举值合法 |
| 断言 | `data["success"] is True` |
| **结果** | ✅ **PASS** |

---

#### TC-CONTACT-04：空白姓名拦截

| 字段 | 内容 |
|------|------|
| 请求体 | `{"name":"   ","email":"test@example.com","message":"留言内容"}` |
| 预期 | HTTP 422，Pydantic 校验拦截 |
| 说明 | 姓名去除空格后为空字符串，触发 `name_not_empty` validator |
| **结果** | ✅ **PASS** |

---

#### TC-CONTACT-05：无效邮箱格式

| 字段 | 内容 |
|------|------|
| 请求体 | `{"name":"张三","email":"not-email","message":"留言内容"}` |
| 预期 | HTTP 422 |
| 说明 | `EmailStr` 类型严格校验邮箱格式 |
| **结果** | ✅ **PASS** |

---

#### TC-CONTACT-06：空白留言拦截

| 字段 | 内容 |
|------|------|
| 请求体 | `{"name":"张三","email":"test@example.com","message":"   "}` |
| 预期 | HTTP 422 |
| 说明 | 留言去除空格后为空，触发 `message_not_empty` validator |
| **结果** | ✅ **PASS** |

---

#### TC-CONTACT-07：留言超长（2001字符）

| 字段 | 内容 |
|------|------|
| 请求体 | message = `"x" * 2001` |
| 预期 | HTTP 422，超过 2000 字符上限 |
| **结果** | ✅ **PASS** |

---

#### TC-CONTACT-08：姓名超长（101个汉字）

| 字段 | 内容 |
|------|------|
| 请求体 | name = `"张" * 101` |
| 预期 | HTTP 422，超过 100 字符上限 |
| **结果** | ✅ **PASS** |

---

#### TC-CONTACT-09：缺少必填字段

| 字段 | 内容 |
|------|------|
| 请求体 | `{"name":"张三"}`（缺少 email 和 message） |
| 预期 | HTTP 422，Pydantic 必填字段校验 |
| **结果** | ✅ **PASS** |

---

## 四、测试结果汇总

| 模块 | 用例数 | 通过 | 失败 | 通过率 |
|------|-------|------|------|-------|
| 产品接口 | 7 | 7 | 0 | 100% |
| 站点统计 | 2 | 2 | 0 | 100% |
| 联系表单 | 9 | 9 | 0 | 100% |
| **合计** | **18** | **18** | **0** | **100%** |

---

## 五、HTTP 状态码覆盖

| 状态码 | 含义 | 验证用例 |
|-------|------|---------|
| 200 | 请求成功 | TC-PRD-01~05, TC-STAT-01~02, TC-CONTACT-01~03 |
| 404 | 资源不存在 | TC-PRD-06, TC-PRD-07 |
| 422 | 请求参数校验失败 | TC-CONTACT-04~09 |

---

## 六、关键业务规则验证

| 规则 | 验证用例 | 验证结果 |
|------|---------|---------|
| 产品列表只返回摘要字段（不含 description） | TC-PRD-02 | ✅ 通过 |
| 产品详情包含关联的 features/specs/images | TC-PRD-03 | ✅ 通过 |
| 不存在的 slug 返回 404 + 中文提示 | TC-PRD-06, TC-PRD-07 | ✅ 通过 |
| 联系表单提交成功返回含"24小时"的提示语 | TC-CONTACT-01 | ✅ 通过 |
| 空白字符姓名/留言被服务端拦截（非前端校验） | TC-CONTACT-04, TC-CONTACT-06 | ✅ 通过 |
| 邮箱格式服务端严格校验 | TC-CONTACT-05 | ✅ 通过 |
| 留言最大长度 2000 字符 | TC-CONTACT-07 | ✅ 通过 |
| 姓名最大长度 100 字符 | TC-CONTACT-08 | ✅ 通过 |

---

## 七、未覆盖场景（后续建议）

| 场景 | 建议优先级 | 说明 |
|------|----------|------|
| CORS 跨域请求验证 | 中 | 验证 CORS_ORIGINS 配置生效 |
| 高并发表单提交 | 低 | 验证数据库写入无竞争 |
| 超大图片 URL 字段（500字符限制） | 低 | Pydantic String(500) 边界 |
| inquiry_type 非法枚举值 | 中 | 传入 `"invalid"` 应返回 422 |
| 前端页面 E2E 测试 | 高 | 使用 Playwright/Cypress 覆盖完整用户路径 |
