# 操作手册：AI智能终端企业官网

**文档版本：** 1.0  
**日期：** 2026-04-19  
**适用版本：** V2.0（FastAPI + Vue3 + SQLAlchemy 2.0）  
**关联技术方案：** TechSpec-AI智能终端企业官网-V2.0.md

---

## 目录

1. [环境准备](#一环境准备)
2. [首次启动](#二首次启动)
3. [日常开发](#三日常开发)
4. [数据库操作](#四数据库操作)
5. [运行测试](#五运行测试)
6. [API 接口验证](#六api-接口验证)
7. [常见问题排查](#七常见问题排查)
8. [生产部署](#八生产部署)

---

## 一、环境准备

### 1.1 前置条件

| 工具 | 版本要求 | 说明 |
|------|---------|------|
| Conda | 任意 | 推荐 Miniforge / Anaconda |
| Node.js | 18+ | 前端构建工具 |
| Git | 任意 | 版本控制 |

### 1.2 创建 Conda 环境（仅首次）

```bash
conda create -n ai-full-stack python=3.11 -y
conda activate ai-full-stack
```

### 1.3 安装后端依赖

```bash
conda activate ai-full-stack
cd backend
pip install -e ".[dev]"
```

安装后验证关键包：

```bash
python -c "import fastapi, sqlalchemy, aiosqlite, pydantic; print('OK')"
```

### 1.4 安装前端依赖

```bash
cd frontend
npm install
```

---

## 二、首次启动

### 2.1 初始化数据库

进入 `backend/` 目录后执行：

```bash
conda activate ai-full-stack
cd backend
python init_db.py
```

预期输出：
```
Tables created OK
```

> 说明：该命令调用 `Base.metadata.create_all`，幂等操作，表已存在时跳过。

### 2.2 导入初始数据（Seed）

```bash
conda activate ai-full-stack
cd backend
python -m scripts.seed_data
```

预期输出：
```
✓ Seed data inserted: 3 products, 3 site stats
```

> 说明：脚本有幂等保护，若已存在数据则打印提示并跳过。

### 2.3 启动后端服务

```bash
conda activate ai-full-stack
cd backend
uvicorn app.main:app --reload --port 8000
```

成功标志：
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

> 注意：`--reload` 仅限开发环境，文件修改后自动重载。生产环境去掉该参数。

### 2.4 启动前端开发服务器

```bash
cd frontend
npm run dev
```

成功标志：
```
VITE v5.x ready in xxx ms
➜  Local:   http://localhost:5173/
```

打开浏览器访问 `http://localhost:5173` 即可看到完整网站。

---

## 三、日常开发

### 3.1 标准启动顺序

每次开发前按以下顺序启动：

```bash
# 终端 1 — 后端
conda activate ai-full-stack && cd backend && uvicorn app.main:app --reload --port 8000

# 终端 2 — 前端
cd frontend && npm run dev
```

### 3.2 开发时端口说明

| 服务 | 默认端口 | 说明 |
|------|---------|------|
| Vue3 开发服务器 | 5173 | Vite HMR，代理 `/api` 到后端 |
| FastAPI 后端 | 8000 | uvicorn，`--reload` 热重载 |

前端代理配置位于 [frontend/vite.config.ts](../frontend/vite.config.ts)：

```typescript
proxy: {
  '/api': { target: 'http://localhost:8000', changeOrigin: true }
}
```

> 若后端无法启动在 8000，修改 `target` 端口后重启前端即可。

### 3.3 API 文档

开发模式下（`DEBUG=true`）可访问自动生成的 Swagger UI：

```
http://localhost:8000/api/docs
```

启用 Debug 模式：编辑 `backend/.env`：

```
DEBUG=true
```

### 3.4 修改数据库模型后的操作

SQLAlchemy 使用 `create_all`（非 Alembic 迁移），**修改模型后需手动处理**：

**开发环境**（可接受删库重建）：

```bash
# 删除旧数据库
rm backend/db.sqlite3

# 重建表 + 重新导入数据
cd backend
python init_db.py
python -m scripts.seed_data
```

**生产环境**：使用 Alembic 生成迁移脚本（见[第八节](#八生产部署)）。

---

## 四、数据库操作

### 4.1 查看当前数据

```bash
conda activate ai-full-stack
cd backend
python -c "
import asyncio
from app.db.session import async_session_factory, init_db
from sqlalchemy import select, text

async def show():
    await init_db()
    async with async_session_factory() as s:
        rows = (await s.execute(text('SELECT slug, name, is_active FROM products'))).fetchall()
        for r in rows:
            print(r)

asyncio.run(show())
"
```

### 4.2 重置数据库

```bash
cd backend
rm db.sqlite3 db.sqlite3-shm db.sqlite3-wal 2>/dev/null || true
python init_db.py
python -m scripts.seed_data
```

### 4.3 备份数据库

SQLite 数据库为单文件，直接复制即可：

```bash
cp backend/db.sqlite3 backend/db.sqlite3.bak-$(date +%Y%m%d)
```

### 4.4 数据库文件位置

| 文件 | 说明 |
|------|------|
| `backend/db.sqlite3` | 主数据库文件 |
| `backend/db.sqlite3-shm` | 共享内存文件（WAL模式自动生成） |
| `backend/db.sqlite3-wal` | WAL 日志文件（WAL模式自动生成） |

> `-shm` 和 `-wal` 文件在数据库正常关闭后会自动合并消失。

---

## 五、运行测试

### 5.1 运行全部测试

```bash
conda activate ai-full-stack
cd backend
pytest tests/ -v
```

预期结果：
```
15 passed in 0.xx s
```

### 5.2 运行单个测试文件

```bash
pytest tests/test_products.py -v
pytest tests/test_contact.py -v
pytest tests/test_stats.py -v
```

### 5.3 查看测试覆盖率

```bash
pip install pytest-cov  # 若未安装
pytest tests/ --cov=app --cov-report=term-missing
```

### 5.4 测试说明

| 测试文件 | 覆盖接口 | 测试数量 |
|---------|---------|---------|
| `test_products.py` | `GET /api/v1/products`、`GET /api/v1/products/{slug}` | 5 |
| `test_contact.py` | `POST /api/v1/contact` | 7 |
| `test_stats.py` | `GET /api/v1/stats` | 3 |

> 测试使用内存 SQLite（`:memory:`），与生产数据库完全隔离，可放心反复运行。

---

## 六、API 接口验证

### 6.1 产品列表

```bash
curl http://localhost:8000/api/v1/products
```

预期：返回 JSON 数组，含 3 个产品（ai-glasses、ai-robot、ai-toy）。

### 6.2 产品详情

```bash
curl http://localhost:8000/api/v1/products/ai-glasses
curl http://localhost:8000/api/v1/products/ai-robot
curl http://localhost:8000/api/v1/products/ai-toy
```

预期：返回含 `features`、`specs`、`images` 的完整 JSON 对象。

### 6.3 站点统计

```bash
curl http://localhost:8000/api/v1/stats
```

预期：返回 JSON 数组，含多条统计数据（label/value/unit）。

### 6.4 联系表单提交

```bash
curl -X POST http://localhost:8000/api/v1/contact \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","email":"zhangsan@example.com","message":"您好，想了解合作事宜"}'
```

预期：
```json
{"success": true, "message": "提交成功，我们将在24小时内与您联系"}
```

### 6.5 错误码说明

| 状态码 | 场景 |
|-------|------|
| 200 | 请求成功 |
| 404 | 产品 slug 不存在 |
| 422 | 请求参数校验失败（如邮箱格式错误、姓名为空） |
| 500 | 服务端异常（开启 DEBUG 后查看详细日志） |

---

## 七、常见问题排查

### 7.1 后端启动失败：`address already in use`

**现象：** `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`

**原因：** 上一次的 uvicorn 进程未正常退出，端口被占用。

**解决：**

```bash
# Windows — 查找占用进程
wmic process where "name='python.exe'" get ProcessId,CommandLine | findstr uvicorn

# 记录 PID 后终止
taskkill /PID <PID> /F
```

或直接换一个端口启动，并同步修改前端代理：

```bash
# 后端用 8002
uvicorn app.main:app --reload --port 8002
```

同时修改 `frontend/vite.config.ts`：

```typescript
target: 'http://localhost:8002'
```

### 7.2 前端报 500 / API 无法访问

1. 确认后端已启动：`curl http://localhost:8000/api/v1/products`
2. 确认 `vite.config.ts` 中 proxy target 端口与后端一致
3. 重启前端 dev server（修改 vite.config 后需重启才生效）

### 7.3 产品详情返回 404

**原因：** 数据库中无该 slug 的产品，或产品 `is_active=False`。

**排查：**

```bash
cd backend
python -c "
import asyncio
from app.db.session import async_session_factory, init_db
from sqlalchemy import text

async def check():
    await init_db()
    async with async_session_factory() as s:
        rows = (await s.execute(text('SELECT slug, is_active FROM products'))).fetchall()
        for r in rows: print(r)

asyncio.run(check())
"
```

如数据为空，执行 [seed 操作](#22-导入初始数据seed)。

### 7.4 测试报错：`RuntimeError: asyncio mode`

**解决：** 确认 `backend/pyproject.toml` 或 `pytest.ini` 中配置了：

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### 7.5 `email-validator` 未安装导致 422

**现象：** POST /contact 返回 `{"detail":"There was an error parsing the body"}`

**解决：**

```bash
conda activate ai-full-stack
pip install email-validator
```

### 7.6 数据库表不存在

**现象：** `sqlite3.OperationalError: no such table: products`

**解决：** 执行初始化：

```bash
cd backend
python init_db.py
python -m scripts.seed_data
```

---

## 八、生产部署

### 8.1 构建前端静态资源

```bash
cd frontend
npm run build
# 输出目录：frontend/dist/
```

### 8.2 启动后端（生产模式）

```bash
conda activate ai-full-stack
cd backend

# 创建生产环境配置
cat > .env << EOF
DEBUG=false
SECRET_KEY=替换为强随机字符串
DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3
CORS_ORIGINS=https://yourdomain.com
EOF

# 启动（去掉 --reload，指定 worker 数量）
uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
```

> SQLite 不支持多 worker 并发写，生产环境 `--workers` 保持 `1`。如需多 worker，迁移至 PostgreSQL。

### 8.3 Nginx 配置

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # 前端静态资源
    root /var/www/ai-website/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 反向代理
    location /api/ {
        proxy_pass         http://127.0.0.1:8000;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|webp|svg|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 8.4 进程守护（systemd）

创建 `/etc/systemd/system/ai-website.service`：

```ini
[Unit]
Description=AI Website FastAPI Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/ai-website/backend
ExecStart=/opt/conda/envs/ai-full-stack/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable ai-website
systemctl start ai-website
systemctl status ai-website
```

### 8.5 数据库迁移（Alembic）

当模型有变更时，使用 Alembic 生成增量迁移：

```bash
conda activate ai-full-stack
cd backend

# 生成迁移脚本
alembic revision --autogenerate -m "描述变更内容"

# 应用迁移
alembic upgrade head

# 查看当前版本
alembic current

# 回滚一个版本
alembic downgrade -1
```

---

## 附录

### A. 项目目录快速参考

| 路径 | 说明 |
|------|------|
| `backend/app/main.py` | FastAPI 入口，lifespan、CORS、路由注册 |
| `backend/app/core/config.py` | 配置项（读取 .env） |
| `backend/app/api/v1/endpoints/` | 路由处理函数 |
| `backend/app/crud/` | 数据库查询逻辑 |
| `backend/app/models/domain/` | SQLAlchemy ORM 模型 |
| `backend/app/models/schemas/` | Pydantic 请求/响应结构 |
| `backend/app/db/session.py` | AsyncSession 工厂 |
| `backend/scripts/seed_data.py` | 初始数据导入脚本 |
| `backend/tests/` | pytest 单元测试 |
| `backend/.env` | 本地环境变量（不提交 Git） |
| `frontend/src/` | Vue3 源码 |
| `frontend/vite.config.ts` | Vite 配置（含 API 代理端口） |

### B. 环境变量说明

| 变量 | 默认值 | 说明 |
|------|-------|------|
| `DEBUG` | `false` | 开启后显示 SQL 日志 + Swagger UI |
| `SECRET_KEY` | `change-me-in-production` | 生产必须替换 |
| `DATABASE_URL` | `sqlite+aiosqlite:///./db.sqlite3` | 数据库连接字符串 |
| `CORS_ORIGINS` | `http://localhost:5173` | 允许的前端来源，多个用逗号分隔 |

### C. Conda 环境名称

```
ai-full-stack
```

Python 路径（Windows）：`D:\lib\conda\envs\ai-full-stack\python.exe`
