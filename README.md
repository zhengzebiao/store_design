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
docker compose -f deploy/docker-compose.yml up --build
```
