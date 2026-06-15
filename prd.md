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
| `templateId` | `/store_design/edit?templateId=1001` | 编辑指定模板。 |
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
| `title` | 模板名称。 |
| `coverUrl` | 模板封面。 |
| `templateType` | 系统模板、自定义模板。 |
| `scene` | 首页、会员中心、普通页面等。 |
| `status` | 使用中、未使用、不可用。 |
| `price` | 价格，免费模板显示免费。 |
| `updatedAt` | 最近更新时间。 |

### 6.1.3 操作

1. 点击“新建装修”进入 `/store_design/edit?mode=create`。
2. 点击“编辑”进入 `/store_design/edit?mode=edit&templateId={id}`。
3. 点击“复制”进入 `/store_design/edit?mode=copy&templateId={id}`。
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
| 编辑 | `mode=edit&templateId={id}` | 加载指定模板详情并编辑。 |
| 复制 | `mode=copy&templateId={id}` | 加载模板详情后生成新模板数据。 |

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
  key: string
  name: string
  category: string
  icon?: string
  defaultTemplateId?: string
  templates: ComponentTemplate[]
  defaultData: Record<string, unknown>
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
| `pageSize` | 每页数量。 |
| `keyword` | 搜索关键词。 |
| `scene` | 页面场景。 |
| `templateType` | 模板类型。 |
| `status` | 模板状态。 |

Response：

```json
{
  "success": true,
  "data": {
    "items": [],
    "page": 1,
    "pageSize": 20,
    "total": 0
  }
}
```

### 7.2.2 模板详情

`GET /api/store-design/templates/{templateId}`

用途：进入编辑页时加载模板详情、页面配置、组件列表。

### 7.2.3 组件元数据

`GET /api/store-design/components`

用途：获取可拖拽组件库与配置 schema。

### 7.2.4 保存页面

`POST /api/store-design/pages/save`

Request：

```json
{
  "mode": "create",
  "templateId": "",
  "page": {
    "title": "首页装修",
    "scene": "home",
    "settings": {},
    "components": []
  },
  "coverImage": ""
}
```

Response：

```json
{
  "success": true,
  "data": {
    "templateId": "1001",
    "targetUrl": "/store_design/edit?mode=edit&templateId=1001",
    "message": "保存成功"
  }
}
```

### 7.2.5 使用模板

`POST /api/store-design/templates/{templateId}/use`

用途：将指定模板设置为当前使用模板。

### 7.2.6 删除模板

`DELETE /api/store-design/templates/{templateId}`

用途：删除自定义模板。

### 7.2.7 上传资源

`POST /api/store-design/assets/upload`

用途：上传封面图、分享图、组件图片等资源。

## 8. Python 后端设计

## 8.1 分层结构

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

## 8.2 推荐领域模型

### store_design_template

| 字段 | 说明 |
| --- | --- |
| `id` | 模板 ID。 |
| `title` | 模板名称。 |
| `template_type` | 系统模板、自定义模板。 |
| `scene` | 页面场景。 |
| `cover_url` | 封面图。 |
| `price` | 模板价格。 |
| `status` | 使用状态。 |
| `is_active` | 是否当前使用。 |
| `created_at` | 创建时间。 |
| `updated_at` | 更新时间。 |

### store_design_page

| 字段 | 说明 |
| --- | --- |
| `id` | 页面 ID。 |
| `template_id` | 所属模板 ID。 |
| `title` | 页面名称。 |
| `scene` | 页面场景。 |
| `settings_json` | 页面配置 JSON。 |
| `components_json` | 组件树 JSON。 |
| `schema_version` | 数据协议版本。 |
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

## 9. 数据校验与版本

1. 装修页面数据增加 `schemaVersion`，首期为 `1`。
2. 组件保存前校验 `key`、`data`、`style`、`children`。
3. 后端保存前校验组件是否存在、schema 是否匹配。
4. 前端加载未知组件时显示非法组件占位，并允许删除。
5. 后续组件协议升级时通过 `schemaVersion` 做迁移。

## 10. 前端工程结构

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

## 11. 数据协议

## 11.1 模板列表项

```ts
interface StoreTemplate {
  id: string
  title: string
  coverUrl?: string
  templateType: 'system' | 'custom'
  scene: 'home' | 'member' | 'custom'
  status: 'active' | 'inactive' | 'disabled'
  price?: string
  updatedAt?: string
}
```

## 11.2 装修页面

```ts
interface StoreDesignPage {
  id?: string
  templateId?: string
  title: string
  scene: 'home' | 'member' | 'custom'
  settings: PageSettings
  components: DesignComponent[]
  schemaVersion: number
}
```

## 11.3 装修组件

```ts
interface DesignComponent {
  id: string
  key: string
  name: string
  templateId?: string
  data: Record<string, unknown>
  style: Record<string, unknown>
  children?: DesignComponent[]
  invalid?: boolean
  invalidReason?: string
}
```

## 12. 交互流程

## 12.1 首页加载流程

```text
用户进入 /store_design/home
  -> React 调用 GET /api/store-design/templates
  -> Python Service 查询模板数据
  -> Python 返回标准分页结果
  -> React 渲染模板卡片列表
```

## 12.2 编辑页加载流程

```text
用户进入 /store_design/edit?mode=edit&templateId=xxx
  -> React 并行请求模板详情和组件元数据
  -> Python Service 查询页面、模板、组件配置
  -> Python 返回标准装修协议
  -> React 初始化编辑器状态
```

## 12.3 保存流程

```text
用户点击保存
  -> React 校验页面配置和组件配置
  -> React 调用 POST /api/store-design/pages/save
  -> Python Service 校验 payload
  -> Python 保存模板、页面配置和组件树
  -> 保存成功后返回 templateId 和 targetUrl
  -> React 提示成功并跳转或停留编辑
```

## 13. 验收标准

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

## 14. 风险与应对

| 风险 | 影响 | 应对 |
| --- | --- | --- |
| 组件 schema 设计不稳定 | 前端配置表单频繁调整 | 先定义核心组件协议，schema 增加版本字段。 |
| 装修 JSON 结构复杂 | 保存和回显不一致 | 前后端共用 TypeScript/Pydantic 协议文档，增加回归用例。 |
| 子应用样式污染 | 影响主应用 | CSS Modules + qiankun 样式隔离。 |
| 拖拽编辑器复杂度高 | 开发周期延长 | 分阶段交付：先单层拖拽，再支持嵌套组件。 |
| 暂无鉴权 | 存在误操作风险 | 限定环境访问，后续增加鉴权中间件。 |
| 新旧入口切换认知成本 | 用户找不到新页面 | 菜单直接配置新入口，不暴露旧入口。 |

## 15. 里程碑建议

| 阶段 | 周期 | 产出 |
| --- | --- | --- |
| 方案确认 | 1-2 天 | 路由、API 契约、数据模型确认。 |
| 子应用骨架 | 2-3 天 | React + qiankun + `/store_design` 路由。 |
| 后端骨架 | 2-3 天 | FastAPI 分层结构、OpenAPI、统一响应、错误处理。 |
| 数据模型与接口 | 4-6 天 | templates/pages/components/assets 接口。 |
| 首页开发 | 3-5 天 | `/store_design/home` 可用。 |
| 编辑器开发 | 2-3 周 | `/store_design/edit` 核心编辑、保存可用。 |
| 联调验收 | 1 周 | 前后端联调、主应用接入、验收报告。 |

## 16. 待确认问题

1. Python 后端是否新建独立服务，还是并入现有后端工程？
2. 数据库是否沿用现有 MySQL 实例，还是新建库表？
3. 组件元数据首期由数据库维护，还是由配置文件初始化导入数据库？
4. 上传资源使用本地存储、对象存储，还是复用现有文件服务？
5. 无鉴权阶段是否限定 IP、环境或企业范围？
6. 保存失败时是否需要导出前端装修 JSON 供人工恢复？
