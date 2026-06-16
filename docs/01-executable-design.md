# 可执行设计总览

## 阶段目标

当前阶段把 PRD 转换为可编码、可测试、可部署的工程方案。优先交付最小闭环: 子应用可访问、后端接口可用、首页可展示、编辑器可保存和回显。

## MVP 范围

| 模块 | P0 能力 | 验收标准 |
| --- | --- | --- |
| 前端骨架 | React + Vite + TypeScript + qiankun | `/store_design/home` 和 `/store_design/edit` 可访问。 |
| 首页 | 模板列表、搜索、刷新、进入编辑 | 能消费 Python 后端模板接口。 |
| 编辑器 | 三栏布局、组件面板、单层组件编辑 | 可创建、编辑、复制基础页面。 |
| 后端 | FastAPI 分层、统一响应、P0 REST API | `/docs`、`/health` 和核心接口可用。 |
| 数据 | 模板、页面、组件元数据、资产模型 | 字段语义与 PRD 保持一致。 |
| 部署 | Dockerfile、docker-compose、CI | 本地容器可启动，CI 可构建。 |

## 落地原则

1. 不兼容旧前端页面和旧路由。
2. 前端只调用 `/api/store-design/*` 新接口。
3. API 字段沿用 `id`、`diy_id`、`datas`、`page_info` 等业务字段。
4. 后端负责 JSON 规范化、默认值补齐和参数校验。
5. 编辑器先实现单层拖拽，再扩展嵌套组件和复杂动态表单。

## 接口优先级

| 接口 | 优先级 | 说明 |
| --- | --- | --- |
| `GET /health` | P0 | 部署健康检查。 |
| `GET /api/store-design/templates` | P0 | 首页模板列表。 |
| `GET /api/store-design/templates/{id}` | P0 | 编辑页详情。 |
| `GET /api/store-design/components` | P0 | 组件元数据。 |
| `POST /api/store-design/pages/save` | P0 | 创建、编辑、复制保存。 |
| `POST /api/store-design/templates/{id}/use` | P1 | 使用模板。 |
| `DELETE /api/store-design/templates/{id}` | P1 | 删除模板。 |
| `POST /api/store-design/assets/upload` | P1 | 资源上传。 |

## 关键约束

- 首页列表 `id` 是模板 ID。
- 编辑页 URL 参数 `id` 是模板 ID。
- 详情响应 `id` 是页面记录 ID。
- 详情响应 `diy_id` 是模板 ID。
- 前端 store 同时保留 `route_id`、`id`、`diy_id`。
- 后端返回 `datas`、`level` 为数组，`page_info`、`top_id`、`foot_id` 为对象。
