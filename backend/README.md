# store-design-api

FastAPI 后端服务，提供店铺装修模板、页面、组件元数据和资源接口。

## 本地数据库初始化

确保 `.env` 中 `DATABASE_URL` 指向 PostgreSQL，例如：

```env
DATABASE_URL=postgresql+psycopg://store_design:store_design@localhost:5432/store_design
```

初始化表结构：

```bash
alembic upgrade head
```

写入默认模板、默认页面和组件元数据：

```bash
py scripts/seed_store_design.py
```

启动服务：

```bash
py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 数据库说明

- Alembic 迁移位于 `migrations/versions/`。
- 初始迁移会创建 `store_design_template`、`store_design_page`、`store_design_component_meta`、`store_design_asset`、`store_design_operation_log`。
- Seed 数据位于 `app/seed/store_design_seed.py`。
- Seed 脚本按业务 key 做 upsert，可重复执行。

## 测试

```bash
py -m pytest
```

测试使用临时 SQLite 内存数据库，并通过 `seed_store_design` 初始化测试数据。
