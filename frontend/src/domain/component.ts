export type ComponentTemplate = {
  id: number | string
  component_key: string
  name: string
  name_en?: string
}

export type ComponentMeta = {
  id: number | string
  component_key: string
  name: string
  category_id?: number | string
  icon?: string
  tpl_id?: number | string
  templates: ComponentTemplate[]
  schema_json?: Record<string, unknown>
  default_data?: Record<string, unknown>
  enabled?: 0 | 1
  sort?: number
}

export type DesignComponent = {
  id: string
  component_key: string
  component_title: string
  template_id: number | string
  remote_data: Record<string, unknown>
  tasks?: DesignComponent[]
  invalid?: boolean
  invalidReason?: string
}
