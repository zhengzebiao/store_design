# 工程骨架设计

## 仓库目录

```text
store_design/
  frontend/
  backend/
  deploy/
  docs/
  .github/workflows/
  .env.example
  prd.md
```

## 前端骨架

```text
frontend/
  src/api/          # 请求客户端和接口封装
  src/app/          # App 和 router
  src/config/       # 运行时配置
  src/domain/       # 类型、序列化、规范化
  src/pages/home/   # 模板首页
  src/pages/edit/   # 装修编辑器
  src/store/        # Zustand store
  src/styles/       # 全局样式和变量
```

## 后端骨架

```text
backend/
  app/api/routes/   # REST 路由
  app/core/         # 配置、数据库、响应、错误
  app/models/       # SQLAlchemy 模型
  app/repositories/ # 数据访问层
  app/schemas/      # Pydantic schema
  app/services/     # 业务服务层
  tests/            # pytest
```

## 下一步

1. 安装前端依赖并运行 `npm run dev`。
2. 安装后端依赖并运行 `uvicorn app.main:app --reload`。
3. 将后端 in-memory repository 替换为 PostgreSQL repository。
4. 补充 Alembic 迁移和真实 seed 数据。
