# Travel Agent

本项目当前仅包含单 Agent 项目的本地基础设施，尚未实现 Agent、提示词、
LangGraph workflow、RAG pipeline 或前端。所有检查均不调用 OpenAI API。

本项目使用标准 CPython 3.11 x64 创建虚拟环境，不使用 Anaconda 作为 base。
此前 Anaconda 自带的旧 MSVC runtime 导致 Chroma 原生写入崩溃；解决方式是
隔离 Python 解释器，不修改 Anaconda、不复制 DLL，也不改变 DLL 搜索顺序。

## Prerequisites

- Git for Windows
- 标准 CPython 3.11 x64（本机安装为官方 CPython 3.11.9）
- Node.js 24 LTS + npm（预留给后续前端，本阶段无需 npm install）
- Docker Desktop，使用 WSL 2 后端和 Linux containers
- PowerShell；localhost 的 5432、6379、8000 端口可用

先打开 Docker Desktop，等待 Engine running。可用 `docker info` 检查。
若安装后已有终端找不到命令，关闭该终端窗口再重新打开。

## First-time Setup

克隆或复制项目后，进入包含本 README 的 `agent-project` 根目录。
以下命令适用于 Windows PowerShell。先明确标准 CPython 安装位置，不能依赖
未激活虚拟环境时的 `python`：它可能仍然指向 Anaconda。
示例使用官方安装器的默认当前用户路径；若安装在其他位置，请调整 `$cpython`。

```powershell
$cpython = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python311\python.exe'
& $cpython --version
& $cpython -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable); print(sys.base_prefix)"
python -m pip install -r requirements.txt
Copy-Item .env.example .env
docker compose config --quiet
docker compose up -d --wait --wait-timeout 120
docker compose ps
python scripts/check_environment.py
pytest
ruff check .
python -m uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
```

仅在 `.env` 尚不存在时执行复制，避免覆盖已有配置。
仅在 `.venv` 内升级构建工具（可选，初始化时已执行）：

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip --version
where.exe python
```

确认 `sys.executable` 位于项目 `.venv`，`sys.base_prefix` 位于标准 CPython 安装目录。
本机 CPython 采用当前用户安装，未加入 PATH，也未安装 Python Launcher。
CPython 3.11.9 是 3.11 系列最后提供传统官方 Windows 安装器的版本；后续 3.11
安全版本只提供源码，不应将 3.11.9 理解为最新安全补丁版。
虚拟环境不能直接跨电脑复制；移动项目后，重新创建 `.venv` 并安装 requirements。
项目源码与配置不依赖用户目录绝对路径。

### Dependencies

`requirements.txt` 是唯一依赖版本来源，锁定本次验证的直接和传递依赖，
目标平台为 Windows x64 / Python 3.11。包含运行依赖及 pytest、pytest-asyncio、Ruff。
保留 `uvicorn[standard]` 与 `psycopg[binary]` extras。
`pyproject.toml` 管理元数据、Python 版本、pytest 和 Ruff；动态读取同一 requirements，
不维护第二套版本。日常无需 `pip install -e .`。

升级依赖时应在项目 `.venv` 内有意识地升级并通过所有检查，再更新锁定文件；
不要每次启动开发环境都升级。Chroma 的传递依赖可能包括 NumPy、ONNX Runtime
和 tokenizers；不额外安装 PyTorch、TensorFlow、transformers 或模型。

### Environment Variables

`.env.example` 是公开示例，`.env` 是本地配置且被 Git 忽略。
`OPENAI_API_KEY` 在本阶段保持空值，不需要 Key 即可运行全部验收。
不要将真实凭据加入源码或 README。

`Settings` 使用 pydantic-settings，从项目根目录 `.env` 加载；普通系统环境变量
优先于文件。密码和 Key 使用 `SecretStr`，模块 import 不发起网络访问。
smoke test 显式使用空 OpenAI Key，不检查机器上其他位置的 Key。
Chroma 的相对路径始终相对于项目根目录，切换当前目录不会改变数据位置。

`POSTGRES_PASSWORD=change_me` 仅为本地示例，请按需在 `.env` 修改。
PostgreSQL 已有数据卷时，修改 `.env` 不会自动更改数据库中的密码。
不要通过删除数据卷解决已有数据的密码问题。

`APP_HOST`、`APP_PORT` 可由 Settings 读取；Uvicorn 命令行参数控制实际监听地址，
修改这两个设置时也要调整启动命令。`/health` 仅检查进程，不访问配置、数据库或 Redis。

## Infrastructure and Checks

Compose 只运行 PostgreSQL 16 和 Redis 7，端口仅绑定 `127.0.0.1`。
PostgreSQL 使用 named volume `postgres_data`，不创建业务表。
Redis 当前为临时测试基础设施，不保证重建容器后数据保留，不配置应用缓存。
Chroma 直接在 Windows 上使用 `PersistentClient`，数据保存在 `chroma_data/`。

```powershell
docker compose config --quiet
docker compose up -d --wait --wait-timeout 120
docker compose ps
python scripts/check_environment.py
```

`config --quiet` 验证完整 Compose 配置但不打印展开后的数据库密码。
若服务不健康，停止下一步并查看 `docker compose logs --tail 100 postgres redis`。
若端口占用，可修改 `.env` 的 PostgreSQL/Redis 端口后重新启动。

smoke test 验证 Python 3.11、项目虚拟环境、配置、三个框架 import、PostgreSQL
`SELECT 1`、Redis PING/SET/GET/DEL、Chroma collection CRUD 和向量查询。
Chroma 使用固定手工向量，禁用 embedding function 和匿名遥测。
临时 Redis key 带过期时间并在 finally 中删除；Chroma 临时 collection 同样在
finally 中清理，不修改已有 collection。任何失败都返回非零退出码。
错误仅输出异常类型，避免日志泄露连接凭据。

成功标志为 `ENVIRONMENT CHECK PASSED`。

## Daily Development

1. 打开 Docker Desktop，等待 Engine running。
2. 在项目根目录打开 PowerShell，执行：

```powershell
.\.venv\Scripts\Activate.ps1
docker compose up -d --wait --wait-timeout 120
python -m uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
```

访问 <http://127.0.0.1:8000/health>，应返回 HTTP 200：

```json
{"status": "ok", "service": "travel-agent-backend"}
```

也可在 `backend` 目录执行 `python -m uvicorn app.main:app --reload`。
不需要修改系统 `PYTHONPATH`。

在另一个新 PowerShell 的项目根目录执行质量和环境检查：

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/check_environment.py
pytest
ruff check .
docker compose ps
git status --short
git check-ignore .env
```

## Shutdown

在运行 Uvicorn 的终端按 Ctrl+C，然后：

```powershell
docker compose down
deactivate
```

`docker compose down` 保留 PostgreSQL named volume。
不要默认使用 `docker compose down -v`：`-v` 会删除数据库数据。
本项目不配置远程仓库、不自动 commit 或 push。
