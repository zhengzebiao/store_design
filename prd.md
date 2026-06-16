# 店铺装修 React + Python + qiankun 重构 PRD

## 1. 背景

本次重构不考虑旧版前端、旧版后端兼容，也不保留旧入口。目标是新建一套店铺装修微前端子应用，通过 React 重构模板首页和装修编辑页，通过 Python 后端提供稳定接口和业务数据服务。

新路由：

- 模板首页：`/store_design/home`
- 装修编辑页：`/store_design/edit`

## 2. 项目目标

### 2.1 产品目标

1. 新建店铺装修微前端子应用，承接店铺模板选择、创建、编辑、保存流程。
2. 使用 React 重构 `/store_design/home` 模板首页。
3. 使用 React 重构 `/store_design/edit` 装修编辑页。
4. 使用 Python 重构后端接口层，对前端提供稳定、结构化 API。
5. 后端按标准服务化方案建设，包含业务服务层、数据访问层、数据模型和接口文档。
6. 当前阶段不需要鉴权，但保留后续鉴权扩展位。

### 2.2 非目标

1. 不迁移旧 Vue 页面。
2. 不兼容旧路由 `/home/modular/shop-template`、`/design`。
3. 不复用旧前端页面结构。
4. 不实现多人实时协作。
5. 不在首期重构主应用全部菜单和权限系统。

## 3. 路由规划

| 页面 | 新路由 | 说明 |
| --- | --- | --- |
| 店铺装修首页 | `/store_design/home` | 模板列表、选择模板、新建装修入口。 |
| 店铺装修编辑页 | `/store_design/edit` | 拖拽装修、组件配置、页面保存。 |

编辑页参数建议：

| 参数 | 示例 | 说明 |
| --- | --- | --- |
| `id` | `/store_design/edit?id=1001` | 模板 ID，对应列表字段 `id`，编辑详情查询时作为 `diy_id`。 |
| `mode` | `create/edit/copy` | 创建、编辑、复制。 |
| `scene` | `home/member/custom` | 页面场景。 |

## 4. 技术方案选型

### 4.1 总体架构

```text
主应用
  └─ qiankun 注册 store_design 子应用
       └─ 挂载路径 /store_design
           ├─ 子应用内部路由 /home -> 最终访问 /store_design/home
           └─ 子应用内部路由 /edit -> 最终访问 /store_design/edit

React 子应用 store_design
  ├─ 模板首页
  ├─ 装修编辑器
  ├─ 组件协议层
  └─ API SDK
          │
          ▼
Python 后端 API 服务
  ├─ templates API
  ├─ pages API
  ├─ components API
  ├─ media API
  ├─ service 业务编排层
  ├─ repository 数据访问层
  └─ database / storage
```

### 4.2 前端选型

| 方向 | 选型 | 理由 |
| --- | --- | --- |
| 框架 | React 18 + TypeScript | 适合复杂配置化编辑器，类型约束清晰。 |
| 构建 | Vite | 启动快，微前端构建配置简单。 |
| 微前端 | qiankun | 可作为独立子应用并入主应用。 |
| UI 组件 | Ant Design 5 | 后台表格、卡片、表单、弹窗能力完整。 |
| 状态管理 | Zustand + Immer | 简洁、适合设计器状态更新。 |
| 请求层 | TanStack Query | 统一接口缓存、刷新、错误状态。 |
| 拖拽 | dnd-kit | 支持排序、拖入、嵌套结构和自定义拖拽体验。 |
| 表单校验 | Ant Design Form + Zod | 组件 schema 动态表单与保存前校验。 |
| 样式 | CSS Modules + Less | 隔离子应用样式，减少主应用污染。 |
| 截图 | html2canvas | 用于生成模板封面或预览图。 |

### 4.3 后端选型

| 方向 | 选型 | 理由 |
| --- | --- | --- |
| Web 框架 | FastAPI | 接口开发快，类型清晰，自动生成 OpenAPI。 |
| 数据校验 | Pydantic v2 | 对接口入参与出参、装修 JSON 做结构化校验。 |
| 服务分层 | Router + Service + Repository | 保持清晰后端架构，便于测试和扩展。 |
| ORM | SQLAlchemy 2.x | 成熟稳定，适合承接模板、页面、组件等业务模型。 |
| 数据库 | MySQL | 适合业务数据持久化，便于与现有系统生态对接。 |
| 迁移 | Alembic | 管理新增表和字段版本。 |
| 缓存 | Redis 可选 | 缓存组件元数据、模板分类等低频数据。 |
| 接口文档 | OpenAPI / Swagger | 前后端契约清晰。 |
| 测试 | pytest + httpx | 覆盖接口、服务逻辑和数据转换。 |

### 4.4 后端定位

后端保持正常工程化后端方案：

1. 对前端暴露稳定 REST API。
2. 在 Service 层处理业务逻辑、参数校验、错误处理、数据标准化。
3. 在 Repository 层处理数据库访问和存储服务访问。
4. 通过 Pydantic schema 约束装修页面、组件配置、模板数据。
5. 通过 OpenAPI 固化前后端接口契约。

## 5. qiankun 微前端方案

### 5.1 子应用信息

- 子应用名称：`store_design`
- 本地端口：`5174`
- 主应用挂载路径：`/store_design`
- 子应用内部首页路由：`/home`
- 子应用内部编辑路由：`/edit`
- 生产资源前缀：`/micro-apps/store_design/`

### 5.2 子应用生命周期

```ts
export async function bootstrap() {}
export async function mount(props: MicroAppProps) {}
export async function unmount() {}
```

### 5.3 主应用注册建议

```js
registerMicroApps([
  {
    name: 'store_design',
    entry: process.env.STORE_DESIGN_ENTRY,
    container: '#micro-app-container',
    activeRule: '/store_design',
    props: {
      basename: '/store_design',
      apiBaseUrl: process.env.STORE_DESIGN_API,
      noAuth: true,
    },
  },
])
```

### 5.4 子应用路由

子应用内部只维护 `/home` 和 `/edit`，由 `basename: '/store_design'` 组合成最终访问地址 `/store_design/home` 和 `/store_design/edit`。

```tsx
const routes = [
  {
    path: '/home',
    element: <StoreDesignHome />,
  },
  {
    path: '/edit',
    element: <StoreDesignEditor />,
  },
]
```

## 6. 功能需求

## 6.1 `/store_design/home` 模板首页

### 6.1.1 页面布局

页面包含：

1. 顶部标题区：店铺装修。
2. 操作区：新建装修、刷新数据。
3. 筛选区：模板类型、页面场景、关键词。
4. 模板卡片列表。
5. 分页区。
6. 空状态、加载状态和错误状态。

### 6.1.2 模板卡片字段

每个模板展示：

| 字段 | 说明 |
| --- | --- |
| `id` | 模板 ID。 |
| `name` | 模板名称。 |
| `head_img` | 模板封面。 |
| `type` | 模板类型，例如 `diy`。 |
| `is_sel` | 是否使用中。 |
| `is_open_tabbar` | 是否开启底部导航。 |
| `system_recommend_template` | 是否系统推荐模板。 |
| `pid` | 参考模板或复制来源。 |
| `price` | 价格，免费模板显示免费。 |
| `updated_at` | 最近更新时间。 |

### 6.1.3 操作

1. 点击“新建装修”进入 `/store_design/edit?mode=create`。
2. 点击“编辑”进入 `/store_design/edit?mode=edit&id={id}`。
3. 点击“复制”进入 `/store_design/edit?mode=copy&id={id}`。
4. 点击“使用模板”调用 Python 后端接口使模板生效。
5. 点击“删除”删除自定义模板。
6. 点击“刷新数据”重新拉取模板列表。

### 6.1.4 列表状态

1. 首次进入自动拉取模板数据。
2. 加载中展示骨架屏或 loading。
3. 加载失败展示失败原因和重试按钮。
4. 无数据展示空状态。
5. 操作成功后刷新当前分页。

## 6.2 `/store_design/edit` 装修编辑页

### 6.2.1 页面布局

编辑器采用三栏布局：

1. 左侧组件面板：组件分类和组件列表。
2. 中间预览画布：移动端页面预览，支持拖拽排序。
3. 右侧配置面板：页面配置、组件配置。
4. 顶部工具栏：返回、模板名称、保存、预览、刷新。

### 6.2.2 页面模式

| 模式 | 参数 | 行为 |
| --- | --- | --- |
| 创建 | `mode=create` | 初始化空白装修页。 |
| 编辑 | `mode=edit&id={id}` | 加载指定模板详情并编辑。 |
| 复制 | `mode=copy&id={id}` | 加载模板详情后生成新模板数据。 |

### 6.2.3 组件面板

组件来源：React 前端调用 Python 后端组件接口，Python 后端从组件元数据表或配置服务读取后标准化返回。

组件分类建议：

1. 基础组件。
2. 图片媒体。
3. 商品组件。
4. 营销组件。
5. 会员组件。
6. 门店组件。

组件字段：

```ts
interface ComponentMeta {
  component_key: string
  name: string
  category_id?: number | string
  icon?: string
  tpl_id?: number | string
  templates: ComponentTemplate[]
  default_data?: Record<string, unknown>
}
```

### 6.2.4 画布能力

1. 支持从左侧拖入组件。
2. 支持组件上下排序。
3. 支持选中组件并打开右侧配置。
4. 支持删除组件。
5. 支持复制组件。
6. 支持空画布状态。
7. 支持移动端宽度预览。
8. 支持组件非法状态提示。

### 6.2.5 配置能力

页面配置：

- 页面名称。
- 页面标题。
- 页面描述。
- 分享图标。
- 背景色。
- 顶部栏颜色。
- 字体颜色。
- 标题对齐。
- 页面场景。

组件配置：

- 根据后端返回 schema 动态渲染。
- 支持文本、数字、颜色、图片、商品选择、链接选择、开关、单选、多选、列表配置。
- 修改后实时更新预览。

### 6.2.6 保存能力

保存时，React 前端只调用 Python 后端保存接口。Python 后端负责校验装修 JSON、保存页面数据、维护模板状态并返回保存结果。

保存流程：

1. 前端校验页面名称和组件配置。
2. 前端生成标准装修 JSON。
3. 前端生成封面图，可选。
4. 调用 `POST /api/store-design/pages/save`。
5. Python Service 层校验 JSON。
6. Python Repository 层保存模板、页面配置、组件数据。
7. 返回保存结果、模板 ID、编辑 URL。

## 7. 后端接口设计

## 7.1 接口原则

1. 前端只对接 Python 后端接口。
2. Python 后端对前端输出稳定、标准化数据结构。
3. 接口不依赖旧前端路由和旧页面结构。
4. 写接口必须做参数校验和业务校验。
5. 暂不鉴权，但保留 `operator`、`tenant`、`headers` 扩展字段。
6. 后端按标准分层设计，支持后续接入鉴权、审计、发布流程。

## 7.2 API 清单

### 7.2.1 模板列表

`GET /api/store-design/templates`

Query：

| 参数 | 说明 |
| --- | --- |
| `page` | 页码。 |
| `limit` | 每页数量。 |
| `keyword` | 搜索关键词。 |
| `type` | 模板类型，例如 `diy`。 |
| `is_sel` | 是否使用中。 |

Response：

```json
{
  "success": true,
  "data": [],
  "current_page": 1,
  "limit": 20,
  "total": 0
}
```

### 7.2.2 模板详情

`GET /api/store-design/templates/{id}`

用途：进入编辑页时加载模板详情、页面配置、组件列表。路径参数 `id` 对应模板列表字段 `id`，后端按 `diy_id` 查询详情。

### 7.2.3 组件元数据

`GET /api/store-design/components`

用途：获取可拖拽组件库与配置 schema。

### 7.2.4 保存页面

`POST /api/store-design/pages/save`

Request：

```json
{
  "mode": "create",
  "id": "",
  "diy_id": "",
  "page_name": "首页装修",
  "type": "home_page",
  "page_sort": 2,
  "page_scene": 2,
  "page_type": "2",
  "page_info": {},
  "datas": [],
  "head_img": ""
}
```

Response：

```json
{
  "success": true,
  "data": {
    "id": "69",
    "diy_id": "1001",
    "url": "/store_design/edit?mode=edit&id=1001",
    "message": "保存成功"
  }
}
```

### 7.2.5 使用模板

`POST /api/store-design/templates/{id}/use`

用途：将指定模板设置为当前使用模板。

### 7.2.6 删除模板

`DELETE /api/store-design/templates/{id}`

用途：删除自定义模板。

### 7.2.7 上传资源

`POST /api/store-design/assets/upload`

用途：上传封面图、分享图、组件图片等资源。

## 8. 接口字段规范

本项目不兼容旧前端和旧入口，但新接口字段命名直接沿用浏览器 Network 抓到的核心业务字段，避免前后端再做一层字段映射。Python 后端只负责数据校验、JSON 字符串解析、默认值补齐和类型规范化。

经浏览器 Network 校验，旧页面主要涉及两个核心接口：

- 模板首页：`GET /api/v1/theme?page=1&limit=50`
- 装修详情：`GET /api/v1/diy/home?diy_id={id}`

### 8.1 模板列表字段

`GET /api/store-design/templates` 单条数据沿用以下字段：

| 字段 | 说明 |
| --- | --- |
| `id` | 模板 ID，进入编辑页时作为 `diy_id` 查询详情。 |
| `name` | 模板名称。 |
| `type` | 模板类型，例如 `diy`。 |
| `is_sel` | 是否使用中，`1` 表示使用中，`0` 表示未使用。 |
| `created_at` | 创建时间。 |
| `updated_at` | 更新时间。 |
| `is_open_tabbar` | 是否开启底部导航。 |
| `other_company_show` | 是否同步或展示到其他企业。 |
| `pid` | 参考模板或复制来源，`0` 表示无来源。 |
| `head_img` | 模板封面图。 |
| `price` | 模板价格。 |
| `theme_id` | 主题 ID，可为空。 |
| `system_recommend_template` | 是否系统推荐模板。 |

说明：列表接口不额外增加 `scene`、`status`、`templateId`、`coverUrl` 等别名字段；前端直接使用上述字段。

### 8.2 装修详情字段

`GET /api/store-design/templates/{id}` 或 `GET /api/store-design/diy-home?diy_id={id}` 返回装修详情，字段沿用以下结构：

| 字段 | 说明 |
| --- | --- |
| `id` | 装修页面记录 ID。 |
| `diy_id` | 模板 ID，对应模板列表中的 `id`。 |
| `company_id` | 企业 ID。 |
| `type` | 页面类型，例如 `home_page`、`project_page`。 |
| `page_name` | 页面/模板名称。 |
| `datas` | 组件树数组。后端必须把旧 JSON 字符串解析为数组后返回。 |
| `other_company_show` | 是否同步或展示到其他企业。 |
| `page_info` | 页面配置对象。后端必须把旧 JSON 字符串解析为对象后返回。 |
| `member_level` | 可访问会员等级。为空时返回空字符串或空数组，需在接口文档中固定一种。 |
| `level` | 会员等级数组。后端必须把旧 JSON 字符串解析为数组后返回。 |
| `status` | 页面状态。 |
| `created_at` | 创建时间。 |
| `updated_at` | 更新时间。 |
| `page_sort` | 页面端类型/页面分类。 |
| `page_scene` | 页面场景。 |
| `top_id` | 顶部菜单配置。 |
| `foot_type` | 底部导航类型。 |
| `foot_id` | 底部导航配置。 |
| `page_type` | 页面适用端。 |

说明：虽然列表接口和详情接口都存在 `id`，但语义不同；列表 `id` 是模板 ID，详情 `id` 是页面记录 ID，详情 `diy_id` 对应列表 `id`。前端必须按当前页面上下文区分。

### 8.3 组件字段

详情字段 `datas` 解析后为组件数组，组件字段沿用以下结构：

| 字段 | 说明 |
| --- | --- |
| `id` | 组件实例 ID。 |
| `component_key` | 组件唯一标识。 |
| `component_title` | 组件显示名称。 |
| `template_id` | 组件模板 ID。 |
| `remote_data` | 组件业务配置和样式配置。 |
| `tasks` | 嵌套子组件，可选。 |

说明：不再额外转换为 `key/name/data/style/children`；React 编辑器内部也优先使用 `component_key/component_title/template_id/remote_data/tasks`，减少字段转换成本。

### 8.4 仍需规范化的点

1. `datas`、`page_info`、`level` 后端返回时必须是结构化数组/对象，不再返回 JSON 字符串。
2. `member_level` 需要固定返回类型，推荐使用数组；如果为了贴近旧字段可保持字段名不变但值为数组。
3. `top_id`、`foot_id` 需要固定空值形态，推荐空对象 `{}` 或 `null`，不要有时数组有时对象。
4. `is_sel`、`is_open_tabbar`、`system_recommend_template` 保持数字 `0/1`，前端按数字判断。
5. 保存接口也使用同一套字段名，避免保存前再做字段映射。

### 8.5 新接口返回要求

1. `/api/store-design/templates` 返回列表摘要字段，不包含完整组件树。
2. `/api/store-design/templates/{id}` 返回完整编辑字段，包括 `page_info`、`datas`、`level`。
3. 新前端直接依赖抓取到的字段名，不再引入别名字段。
4. Python 后端负责 JSON 字符串解析、类型固定、默认值填充和 Pydantic 校验。
5. 保存接口接收同名字段，后端可直接保存到数据库或转换为原业务存储结构。

## 9. Python 后端设计

## 9.1 分层结构

```text
backend/
  app/
    main.py
    api/
      routes/
        templates.py
        pages.py
        components.py
        assets.py
    schemas/
      template.py
      page.py
      component.py
      asset.py
    services/
      template_service.py
      page_service.py
      component_service.py
      asset_service.py
      normalize_service.py
    repositories/
      template_repository.py
      page_repository.py
      component_repository.py
      asset_repository.py
    models/
      template.py
      page.py
      component.py
      asset.py
    core/
      config.py
      database.py
      cache.py
      response.py
      errors.py
```

## 9.2 推荐领域模型

### store_design_template

| 字段 | 说明 |
| --- | --- |
| `id` | 模板 ID。 |
| `name` | 模板名称。 |
| `type` | 模板类型。 |
| `is_sel` | 是否当前使用。 |
| `is_open_tabbar` | 是否开启底部导航。 |
| `other_company_show` | 是否同步或展示到其他企业。 |
| `pid` | 参考模板或复制来源。 |
| `head_img` | 封面图。 |
| `price` | 模板价格。 |
| `theme_id` | 主题 ID。 |
| `system_recommend_template` | 是否系统推荐模板。 |
| `created_at` | 创建时间。 |
| `updated_at` | 更新时间。 |

### store_design_page

| 字段 | 说明 |
| --- | --- |
| `id` | 页面 ID。 |
| `diy_id` | 所属模板 ID。 |
| `company_id` | 企业 ID。 |
| `type` | 页面类型，例如 `home_page`。 |
| `page_name` | 页面名称。 |
| `datas` | 组件树 JSON/数组。 |
| `page_info` | 页面配置 JSON/对象。 |
| `member_level` | 可访问会员等级。 |
| `level` | 会员等级列表。 |
| `status` | 页面状态。 |
| `page_sort` | 页面端类型/页面分类。 |
| `page_scene` | 页面场景。 |
| `top_id` | 顶部菜单配置。 |
| `foot_type` | 底部导航类型。 |
| `foot_id` | 底部导航配置。 |
| `page_type` | 页面适用端。 |
| `created_at` | 创建时间。 |
| `updated_at` | 更新时间。 |

### store_design_component_meta

| 字段 | 说明 |
| --- | --- |
| `id` | 组件元数据 ID。 |
| `component_key` | 组件唯一标识。 |
| `name` | 组件名称。 |
| `category` | 组件分类。 |
| `icon` | 组件图标。 |
| `schema_json` | 配置 schema。 |
| `default_data_json` | 默认数据。 |
| `enabled` | 是否启用。 |
| `sort` | 排序。 |

## 10. 数据校验与版本

1. 装修页面数据增加 `schemaVersion`，首期为 `1`。
2. 组件保存前校验 `key`、`data`、`style`、`children`。
3. 后端保存前校验组件是否存在、schema 是否匹配。
4. 前端加载未知组件时显示非法组件占位，并允许删除。
5. 后续组件协议升级时通过 `schemaVersion` 做迁移。

## 11. 前端工程结构

```text
store-design/
  package.json
  vite.config.ts
  src/
    main.tsx
    qiankun.ts
    app/
      App.tsx
      router.tsx
    pages/
      home/
        StoreDesignHome.tsx
        TemplateCard.tsx
        TemplateFilters.tsx
      edit/
        StoreDesignEditor.tsx
        ComponentPanel.tsx
        PreviewCanvas.tsx
        PropertyPanel.tsx
        EditorToolbar.tsx
    api/
      client.ts
      templates.ts
      pages.ts
      components.ts
      assets.ts
    domain/
      template.ts
      page.ts
      component.ts
      normalize.ts
      serialize.ts
    store/
      editorStore.ts
    styles/
      variables.less
      global.less
```

## 12. 数据协议

## 12.1 模板列表项

```ts
interface StoreTemplate {
  id: number | string
  name: string
  type: 'diy' | string
  is_sel: 0 | 1
  created_at?: string
  updated_at?: string
  is_open_tabbar?: 0 | 1
  other_company_show?: 0 | 1
  pid?: number | string
  head_img?: string
  price?: string
  theme_id?: number | string | null
  system_recommend_template?: 0 | 1
}
```

## 12.2 装修页面

```ts
interface StoreDesignPage {
  id: number | string
  diy_id: number | string
  company_id?: number | string
  type: 'home_page' | 'project_page' | string
  page_name: string
  datas: DesignComponent[]
  other_company_show?: 0 | 1
  page_info: Record<string, unknown>
  member_level?: number[] | string | null
  level: MemberLevel[]
  status?: number
  created_at?: string
  updated_at?: string
  page_sort?: number | string
  page_scene?: number | string
  top_id?: Record<string, unknown> | null
  foot_type?: number | string
  foot_id?: Record<string, unknown> | null
  page_type?: string | string[]
}
```

## 12.3 装修组件

```ts
interface DesignComponent {
  id: string
  component_key: string
  component_title: string
  template_id: number | string
  remote_data: Record<string, unknown>
  tasks?: DesignComponent[]
  invalid?: boolean
  invalidReason?: string
}
```

## 13. 交互流程

## 13.1 首页加载流程

```text
用户进入 /store_design/home
  -> React 调用 GET /api/store-design/templates
  -> Python Service 查询模板数据
  -> Python 返回标准分页结果
  -> React 渲染模板卡片列表
```

## 13.2 编辑页加载流程

```text
用户进入 /store_design/edit?mode=edit&id=xxx
  -> React 并行请求模板详情和组件元数据
  -> Python Service 查询页面、模板、组件配置
  -> Python 返回标准装修协议
  -> React 初始化编辑器状态
```

## 13.3 保存流程

```text
用户点击保存
  -> React 校验页面配置和组件配置
  -> React 调用 POST /api/store-design/pages/save
  -> Python Service 校验 payload
  -> Python 保存模板、页面配置和组件树
  -> 保存成功后返回 id、diy_id 和 url
  -> React 提示成功并跳转或停留编辑
```

## 14. 验收标准

### 13.1 路由验收

1. `/store_design/home` 能打开模板首页。
2. `/store_design/edit` 能打开装修编辑页。
3. 不再依赖 `/home/modular/shop-template` 和 `/design`。
4. 页面刷新后路由仍可正确加载子应用。

### 13.2 首页验收

1. React 前端只调用 Python 后端接口。
2. 模板列表可正常分页、搜索、筛选。
3. 无数据时展示空状态。
4. 接口失败时展示明确错误和重试入口。
5. 支持进入创建、编辑、复制流程。
6. 支持使用模板、删除模板。

### 13.3 编辑器验收

1. 创建模式可初始化空白页面。
2. 编辑模式可加载真实模板详情。
3. 复制模式不会覆盖原模板。
4. 组件库来自 Python 后端接口。
5. 可拖入、排序、删除、复制组件。
6. 右侧配置修改可实时更新预览。
7. 保存后再次打开数据一致。
8. 保存失败返回真实错误，不伪造成功。

### 13.4 后端验收

1. 后端是标准 FastAPI 服务，对前端提供稳定 REST API。
2. 接口符合 OpenAPI 文档。
3. 写接口具备参数校验和业务校验。
4. 装修 JSON 保存前经过 Pydantic 校验。
5. 模板、页面、组件元数据具备基础测试覆盖。
6. 暂无鉴权时，仍预留租户、操作者和审计扩展字段。

## 15. 容器化与自动部署方案

### 15.1 Docker 容器化目标

1. React 子应用、Python 后端均通过 Docker 镜像交付。
2. 本地、测试、生产环境使用一致的容器运行方式。
3. 支持 GitHub Actions 自动构建镜像、推送镜像、远程服务器部署。
4. 支持一键回滚到上一版本镜像。
5. 所有敏感配置通过环境变量或 GitHub Secrets 注入，不写入代码仓库。

### 15.2 镜像规划

| 服务 | 镜像 | 说明 |
| --- | --- | --- |
| React 子应用 | `store-design-web` | 构建静态资源，由 Nginx 容器提供访问。 |
| Python 后端 | `store-design-api` | FastAPI + Uvicorn/Gunicorn 服务。 |
| Nginx 网关 | `store-design-nginx` 可选 | 统一代理前端静态资源和后端 API。 |

### 15.3 推荐目录结构

```text
store_design/
  frontend/
    Dockerfile
    nginx.conf
  backend/
    Dockerfile
    app/
  deploy/
    docker-compose.yml
    docker-compose.prod.yml
    nginx.conf
  .github/
    workflows/
      deploy.yml
```

### 15.4 Dockerfile 建议

React 子应用镜像：

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

Python 后端镜像：

```dockerfile
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 15.5 docker-compose 部署建议

```yaml
services:
  store-design-web:
    image: ${REGISTRY}/store-design-web:${IMAGE_TAG}
    restart: always
    ports:
      - "8080:80"
    depends_on:
      - store-design-api

  store-design-api:
    image: ${REGISTRY}/store-design-api:${IMAGE_TAG}
    restart: always
    env_file:
      - .env
    ports:
      - "8000:8000"
```

### 15.6 测试环境与生产环境区分

| 项目 | 测试环境 | 生产环境 |
| --- | --- | --- |
| GitHub Environment | `test` | `production` |
| 触发分支 | `develop` 或 `test` | `main` 或 release tag |
| 是否自动部署 | 自动部署 | 建议人工审批后部署 |
| 镜像 tag | `test-${GITHUB_SHA::7}` | `prod-${GITHUB_SHA::7}` 或 `vX.Y.Z` |
| 服务器目录 | `/opt/store_design_test` | `/opt/store_design_prod` |
| 环境变量文件 | `.env.test` | `.env.prod` |
| 前端访问域名 | `test-store-design.example.com` | `store-design.example.com` |
| API 地址 | 测试 API / 测试数据库 | 生产 API / 生产数据库 |
| 容器项目名 | `store_design_test` | `store_design_prod` |
| 部署策略 | 快速验证，允许频繁部署 | 稳定发布，部署前备份版本 |

### 15.7 GitHub Actions 自动部署流程

触发方式：

1. PR 阶段只执行 lint、test、build，不部署。
2. `develop` 或 `test` 分支 push 自动部署测试环境。
3. `main` 分支 push 或 release tag 部署生产环境，建议配置 GitHub Environment approval。
4. 支持 `workflow_dispatch` 手动选择部署环境和镜像 tag。

流程：

```text
代码提交
  -> GitHub Actions checkout
  -> 安装依赖
  -> 前端 lint/test/build
  -> 后端 test
  -> 判断部署环境 test/production
  -> 构建带环境前缀的 Docker 镜像 tag
  -> 推送镜像到 GHCR 或私有镜像仓库
  -> SSH 登录对应环境远程服务器
  -> 写入对应环境 IMAGE_TAG 和 .env
  -> docker compose --project-name 对应环境 pull
  -> docker compose --project-name 对应环境 up -d
  -> 执行对应环境健康检查
  -> 部署成功/失败通知
```

### 15.8 GitHub Secrets

建议使用 GitHub Environments 分别维护 `test` 和 `production` 的 Secrets，避免测试环境和生产环境配置混用。

| Secret | 测试环境 | 生产环境 | 说明 |
| --- | --- | --- | --- |
| `DEPLOY_HOST` | 测试服务器地址 | 生产服务器地址 | 远程服务器地址。 |
| `DEPLOY_PORT` | 测试 SSH 端口 | 生产 SSH 端口 | SSH 端口。 |
| `DEPLOY_USER` | 测试部署用户 | 生产部署用户 | SSH 用户。 |
| `DEPLOY_SSH_KEY` | 测试 SSH 私钥 | 生产 SSH 私钥 | SSH 私钥。 |
| `REGISTRY_USERNAME` | 镜像仓库用户名 | 镜像仓库用户名 | 镜像仓库用户名。 |
| `REGISTRY_TOKEN` | 镜像仓库 token | 镜像仓库 token | 镜像仓库访问 token。 |
| `ENV_FILE` | 测试 `.env` 内容 | 生产 `.env` 内容 | 部署时写入服务器的环境变量。 |
| `HEALTHCHECK_URL` | 测试健康检查地址 | 生产健康检查地址 | 部署后校验服务状态。 |

### 15.9 GitHub Actions 示例

```yaml
name: deploy-store-design

on:
  push:
    branches: [develop, test, main]
  workflow_dispatch:
    inputs:
      environment:
        description: Deploy environment
        required: true
        default: test
        type: choice
        options:
          - test
          - production
      image_tag:
        description: Image tag to deploy, optional
        required: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment || (github.ref_name == 'main' && 'production' || 'test') }}
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Resolve deploy environment
        run: |
          if [ "${{ github.event_name }}" = "workflow_dispatch" ]; then
            DEPLOY_ENV="${{ github.event.inputs.environment }}"
          elif [ "${{ github.ref_name }}" = "main" ]; then
            DEPLOY_ENV="production"
          else
            DEPLOY_ENV="test"
          fi
          echo "DEPLOY_ENV=${DEPLOY_ENV}" >> $GITHUB_ENV

      - name: Set image tag
        run: |
          if [ -n "${{ github.event.inputs.image_tag }}" ]; then
            IMAGE_TAG="${{ github.event.inputs.image_tag }}"
          elif [ "$DEPLOY_ENV" = "production" ]; then
            IMAGE_TAG="prod-${GITHUB_SHA::7}"
          else
            IMAGE_TAG="test-${GITHUB_SHA::7}"
          fi
          echo "IMAGE_TAG=${IMAGE_TAG}" >> $GITHUB_ENV

      - name: Build and push web image
        run: |
          docker build -t ghcr.io/${{ github.repository }}/store-design-web:${IMAGE_TAG} ./frontend
          docker push ghcr.io/${{ github.repository }}/store-design-web:${IMAGE_TAG}

      - name: Build and push api image
        run: |
          docker build -t ghcr.io/${{ github.repository }}/store-design-api:${IMAGE_TAG} ./backend
          docker push ghcr.io/${{ github.repository }}/store-design-api:${IMAGE_TAG}

      - name: Deploy to remote server
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          port: ${{ secrets.DEPLOY_PORT }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            if [ "${{ env.DEPLOY_ENV }}" = "production" ]; then
              DEPLOY_DIR="/opt/store_design_prod"
              PROJECT_NAME="store_design_prod"
            else
              DEPLOY_DIR="/opt/store_design_test"
              PROJECT_NAME="store_design_test"
            fi
            cd $DEPLOY_DIR
            printf '%s' '${{ secrets.ENV_FILE }}' > .env
            export IMAGE_TAG=${{ env.IMAGE_TAG }}
            docker compose --project-name $PROJECT_NAME pull
            docker compose --project-name $PROJECT_NAME up -d
            docker image prune -f

      - name: Health check
        run: curl -fsS ${{ secrets.HEALTHCHECK_URL }}
```

### 15.10 远程服务器要求

1. 已安装 Docker Engine 和 Docker Compose Plugin。
2. 测试环境部署目录建议为 `/opt/store_design_test`。
3. 生产环境部署目录建议为 `/opt/store_design_prod`。
4. 两套环境分别保存 `docker-compose.yml`、`.env` 和必要 Nginx 配置。
5. 测试和生产使用不同端口、域名、数据库、对象存储 bucket 和日志目录。
6. 防火墙开放 Web 端口和必要 API 端口。
7. 生产环境建议由统一 Nginx 或网关反代到容器服务。
8. 同一台服务器部署测试和生产时，必须使用不同 compose project name，避免容器名、网络名、volume 冲突。

### 15.11 健康检查与回滚

健康检查：

1. 测试环境检查测试域名下 `/store_design/home`、`/store_design/edit` 和 `/health`。
2. 生产环境检查生产域名下 `/store_design/home`、`/store_design/edit` 和 `/health`。
3. 部署后 GitHub Actions 使用当前环境的 `HEALTHCHECK_URL` 执行 `curl` 校验。
4. 健康检查失败时标记部署失败，并保留当前日志用于排查。

回滚方式：

1. 测试环境允许直接重新部署上一版本 `test-*` 镜像。
2. 生产环境回滚必须使用上一版本 `prod-*` 或 release tag 镜像。
3. 远程服务器分别保存测试和生产上一版本 `IMAGE_TAG`。
4. 回滚时修改对应环境 `.env` 中 `IMAGE_TAG` 为上一版本。
5. 执行 `docker compose --project-name <env_project> pull && docker compose --project-name <env_project> up -d`。
6. 回滚后再次执行对应环境健康检查。

### 15.12 部署验收标准

1. GitHub Actions 能在测试分支提交后自动构建并部署测试环境。
2. GitHub Actions 能在生产分支或 release tag 下部署生产环境。
3. 生产环境部署支持 GitHub Environment 人工审批。
4. 测试和生产镜像 tag 可区分，分别带 `test-`、`prod-` 或版本号前缀。
5. 测试和生产使用不同 Secrets、`.env`、服务器目录和 compose project name。
6. 镜像能成功推送到镜像仓库。
7. Actions 能通过 SSH 登录对应环境远程服务器并更新容器。
8. 部署后对应环境 `/store_design/home`、`/store_design/edit` 可访问。
9. 对应环境后端 `/health` 可访问。
10. 支持通过指定旧 `IMAGE_TAG` 完成测试或生产环境回滚。

## 16. 风险与应对

| 风险 | 影响 | 应对 |
| --- | --- | --- |
| 组件 schema 设计不稳定 | 前端配置表单频繁调整 | 先定义核心组件协议，schema 增加版本字段。 |
| 装修 JSON 结构复杂 | 保存和回显不一致 | 前后端共用 TypeScript/Pydantic 协议文档，增加回归用例。 |
| 子应用样式污染 | 影响主应用 | CSS Modules + qiankun 样式隔离。 |
| 拖拽编辑器复杂度高 | 开发周期延长 | 分阶段交付：先单层拖拽，再支持嵌套组件。 |
| 暂无鉴权 | 存在误操作风险 | 限定环境访问，后续增加鉴权中间件。 |
| 新旧入口切换认知成本 | 用户找不到新页面 | 菜单直接配置新入口，不暴露旧入口。 |
| Docker 镜像构建失败 | 阻断部署 | Actions 中分前端、后端独立构建，保留构建日志和缓存。 |
| 远程服务器部署失败 | 服务不可用 | 部署前备份当前 IMAGE_TAG，失败后自动或手动回滚。 |
| 环境变量泄露 | 安全风险 | 使用 GitHub Secrets 和服务器 `.env`，禁止提交敏感配置。 |
| 测试和生产环境混用 | 数据污染或误发布 | 使用 GitHub Environments、独立 Secrets、独立部署目录和不同镜像 tag。 |

## 17. 里程碑建议

| 阶段 | 周期 | 产出 |
| --- | --- | --- |
| 方案确认 | 1-2 天 | 路由、API 契约、数据模型确认。 |
| 子应用骨架 | 2-3 天 | React + qiankun + `/store_design` 路由。 |
| 后端骨架 | 2-3 天 | FastAPI 分层结构、OpenAPI、统一响应、错误处理。 |
| 数据模型与接口 | 4-6 天 | templates/pages/components/assets 接口。 |
| 首页开发 | 3-5 天 | `/store_design/home` 可用。 |
| 编辑器开发 | 2-3 周 | `/store_design/edit` 核心编辑、保存可用。 |
| 容器化与 CI/CD | 3-5 天 | Dockerfile、docker-compose、GitHub Actions 自动部署。 |
| 联调验收 | 1 周 | 前后端联调、主应用接入、自动部署验收报告。 |

## 18. 待确认问题

1. Python 后端是否新建独立服务，还是并入现有后端工程？
2. 数据库是否沿用现有 MySQL 实例，还是新建库表？
3. 组件元数据首期由数据库维护，还是由配置文件初始化导入数据库？
4. 上传资源使用本地存储、对象存储，还是复用现有文件服务？
5. 无鉴权阶段是否限定 IP、环境或企业范围？
6. 保存失败时是否需要导出前端装修 JSON 供人工恢复？
7. 镜像仓库使用 GHCR、Docker Hub，还是公司私有仓库？
8. 远程服务器部署路径、域名、端口和反向代理规则是什么？
9. GitHub Actions 部署生产环境是否需要人工审批？
10. 测试环境和生产环境分别使用哪些分支触发？
11. 测试环境和生产环境是否部署在同一台服务器？如果是，端口和容器 project name 如何规划？
12. 测试数据库、生产数据库、对象存储 bucket 是否完全隔离？
