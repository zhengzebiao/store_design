# store_design

店铺装修 React + Python + qiankun 重构工程。

## 目录

- `prd.md`: 产品需求文档。
- `docs/`: 可执行设计、任务拆解和工程骨架说明。
- `frontend/`: React 18 + Vite + qiankun 子应用。
- `backend/`: FastAPI 后端服务。
- `deploy/`: Docker Compose 和 Nginx 部署配置。

## 本地启动

### 后端

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
alembic upgrade head
py scripts/seed_store_design.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问:

- 前端首页: http://localhost:5174/store_design/home
- 前端编辑页: http://localhost:5174/store_design/edit?mode=create
- 后端文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### Docker Compose

```bash
cp .env.example .env
docker-compose -f deploy/docker-compose.yml up --build
```

Compose 启动时后端容器默认执行 `alembic upgrade head` 和 seed 数据初始化，可通过 `.env` 设置 `RUN_MIGRATIONS=0` 或 `RUN_SEED=0` 关闭。

访问:

- 容器前端: http://localhost:8080/store_design/home
- 容器后端: http://localhost:8000/health

## 测试环境自动部署

推送到 `master` 或 `test` 分支，或手动运行 `ci` workflow 时，会构建前后端镜像并推送到 GHCR，然后通过 SSH 部署到 GitHub Environment `test` 对应服务器。

服务器需要提前准备：

```text
/opt/store_design_test/docker-compose.yml
```

`docker-compose.yml` 可使用 `deploy/docker-compose.server.yml`，服务器需安装 Docker 和旧版 `docker-compose`。

GitHub Environment `test` 需要配置 Secrets：

- `DEPLOY_HOST`: 测试服务器地址
- `DEPLOY_PORT`: SSH 端口，例如 `22`
- `DEPLOY_USER`: SSH 用户
- `DEPLOY_SSH_KEY`: SSH 私钥
- `ENV_FILE`: 写入服务器 `.env` 的非镜像环境变量内容
- `GHCR_TOKEN`: 可选；如果 GHCR package 是私有的，服务器拉镜像需要这个 token
- `GHCR_USERNAME`: 可选；默认使用触发 workflow 的 GitHub 用户
- `HEALTHCHECK_URL`: 可选；部署后用于 `curl` 检查的地址

可选配置 Variables：

- `DEPLOY_DIR`: 默认 `/opt/store_design_test`
- `COMPOSE_PROJECT_NAME`: 默认 `store_design_test`

