# 项目总览：AI智能终端企业官网 V2.0

**文档版本：** 1.0  
**日期：** 2026-04-20  
**关联技术方案：** TechSpec-AI智能终端企业官网-V2.0.md

---

## 一、项目描述

这是一个 **AI智能终端硬件公司的对外展示型官网**，面向潜在客户、媒体、合作伙伴，提供：

- 企业产品展示（AI眼镜、AI机器人、AI玩具）
- 站点统计数据动态展示
- 联系/合作意向表单收集
- 生产级 API + 前端动效的完整全栈实现

整体采用前后端分离架构：前端 Vue 3 SPA + Vite 构建，后端 FastAPI + SQLAlchemy 2.0 异步 ORM，数据库 SQLite，Nginx 反向代理统一入口。

---

## 二、技术栈

| 层级 | 技术 | 版本 | 职责 |
|------|------|------|------|
| 前端框架 | Vue 3 | 3.4+ | SPA 渲染、路由、状态管理 |
| 构建工具 | Vite | 5.x | 开发服务器、生产打包 |
| 前端路由 | Vue Router | 4.x | 客户端路由 |
| 状态管理 | Pinia | 2.x | 全局状态 |
| 样式 | Tailwind CSS | 3.x | 原子化 CSS，深色主题 |
| 动效 | GSAP | 3.x | 滚动动效、数字计数、Hero 动画 |
| HTTP 客户端 | Axios | 1.x | API 请求封装 |
| API 框架 | FastAPI | 0.115+ | REST API、自动文档（Swagger UI） |
| ORM | SQLAlchemy | 2.0+ | 异步 ORM，Mapped 风格模型定义 |
| 数据库驱动 | aiosqlite | 0.20+ | SQLite 异步驱动 |
| 数据库 | SQLite | 3.x | 轻量级本地持久化 |
| 迁移工具 | Alembic | 1.13+ | 数据库版本管理 |
| ASGI 服务器 | Uvicorn | 0.30+ | FastAPI 生产运行容器 |
| 反向代理 | Nginx | 1.24+ | 静态资源服务 + API 代理 |

---

## 三、数据库设计

### 3.1 表结构关系

```
Product (1) ──< ProductFeature (N)   # 产品特性
Product (1) ──< ProductSpec    (N)   # 产品规格
Product (1) ──< ProductImage   (N)   # 产品图库

ContactSubmission  (独立表)          # 联系表单提交
SiteStat           (独立表)          # 站点统计数字
```

### 3.2 各表说明

| 表名 | 关键字段 | 说明 |
|------|---------|------|
| `products` | `slug`, `category`, `is_active`, `sort_order` | 产品主表，软删除控制，按排序展示 |
| `product_features` | `icon`, `title`, `description` | 产品核心功能点（1对多） |
| `product_specs` | `spec_key`, `spec_value` | 技术规格键值对（1对多） |
| `product_images` | `image_url`, `alt_text` | 产品图片列表（1对多） |
| `contact_submissions` | `name`, `email`, `inquiry_type`, `status`, `ip_address` | 联系表单，含状态流转（pending/replied/closed） |
| `site_stats` | `label`, `value`, `unit`, `is_active` | 官网动态数字展示（如"10M+ 用户"） |

### 3.3 设计要点

- 所有表均含 `id`（主键自增）
- 产品相关子表通过 `product_id` 外键关联，`cascade="all, delete-orphan"` 级联删除
- `is_active` 字段实现软删除/上下架控制
- `sort_order` 字段控制展示顺序
- `created_at` / `updated_at` 自动记录时间戳

---

## 四、接口设计

### 4.1 接口总览

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| GET | `/api/v1/products` | 获取活跃产品列表（轻量，不含子关联） | 无 |
| GET | `/api/v1/products/{slug}` | 获取产品详情（含 features/specs/images） | 无 |
| GET | `/api/v1/stats` | 获取站点统计数字列表 | 无 |
| POST | `/api/v1/contact` | 提交联系意向表单 | 无 |

### 4.2 数据校验规则

| 字段 | 规则 |
|------|------|
| `name` | 非空，≤ 100 字符 |
| `email` | EmailStr 格式校验 |
| `message` | 非空，≤ 2000 字符 |
| `inquiry_type` | 枚举值：`cooperation / media / other` |

### 4.3 响应格式示例

**产品列表（GET /api/v1/products）：**

```json
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

**联系表单提交（POST /api/v1/contact）：**

```json
{"success": true, "message": "提交成功，我们将在24小时内与您联系"}
```

### 4.4 错误码说明

| 状态码 | 场景 |
|--------|------|
| 200 | 请求成功 |
| 404 | 产品 slug 不存在或已下架 |
| 422 | 请求参数校验失败（邮箱格式错误、字段为空等） |
| 500 | 服务端异常（开启 DEBUG 后查看详细日志） |

---

## 五、已完成功能

| 模块 | 完成情况 |
|------|---------|
| 后端 FastAPI + SQLAlchemy 2.0 Async 架构搭建 | ✅ 完成 |
| 数据库模型设计（6 张表） | ✅ 完成 |
| 全部 4 个 REST API 接口实现 | ✅ 完成 |
| Alembic 数据库迁移管理 | ✅ 完成 |
| Seed 初始数据脚本（3 产品 + 3 统计）| ✅ 完成 |
| Pydantic 请求校验 + 响应序列化 | ✅ 完成 |
| pytest 单元测试（15 个用例，全部通过）| ✅ 完成 |
| Vue 3 前端完整页面（首页/产品/关于/联系）| ✅ 完成 |
| Vite 开发代理 + 生产构建 | ✅ 完成 |
| Nginx 反向代理配置模板 | ✅ 完成 |
| Docker 容器化部署配置 | ✅ 完成 |

**当前状态：** 后端 API + 测试已完整交付，前端页面和 Docker 部署已就绪，整体达到**可生产部署**状态。

---

## 六、待增强方向

| 优先级 | 方向 | 说明 |
|--------|------|------|
| 🔴 高 | 联系表单状态管理 | `status` 字段已有（pending/replied/closed），缺管理后台或通知机制 |
| 🔴 高 | 图片资源管理 | 当前 `image_url` 为字符串路径，需对接实际图片存储（本地 static 或 OSS） |
| 🟡 中 | 接口限流 | `POST /contact` 无防刷机制，需加 IP 频率限制（slowapi + Redis） |
| 🟡 中 | 邮件通知 | 表单提交后自动发邮件给运营（集成 SMTP / SendGrid） |
| 🟡 中 | SEO 优化 | 前端需补充完整 `<meta>` 标签 + Open Graph + sitemap.xml |
| 🟢 低 | 前端动效完善 | GSAP 滚动触发、数字 Count-Up 动画需实际调试打磨 |
| 🟢 低 | 测试覆盖率提升 | 当前 15 个用例，缺少边界测试和集成测试场景 |

---

## 七、未来扩展方向

| 方向 | 技术路径 | 说明 |
|------|---------|------|
| 多语言国际化 | Vue i18n | 支持中英文切换，面向海外市场 |
| 后台管理系统 | FastAPI Admin / 独立 Vue 后台 | 管理产品内容、查看和处理联系表单 |
| 数据库升级 | PostgreSQL + asyncpg | SQLite 不支持多 worker，高并发场景需迁移 |
| 搜索功能 | MeiliSearch / Elasticsearch | 产品内容全文检索 |
| 用户系统 | JWT + OAuth2 | 经销商/合作伙伴专属登录区域 |
| CDN + 媒体存储 | 阿里云 OSS / AWS S3 | 产品图片、视频资源云端托管 |
| 移动端 App | uni-app / React Native | 复用后端 API，扩展到移动端 |
| 数据分析 | 埋点 + BI 报表 | 用户行为分析、产品热度追踪 |

---

*文档生成时间：2026-04-20*
