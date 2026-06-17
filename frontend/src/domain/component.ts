export type ComponentTemplate = {
  id: number | string
  component_key: string
  name: string
  name_en?: string
}

export type ComponentSchemaField = {
  key: string
  label: string
  type: 'text' | 'textarea' | 'number' | 'color' | 'switch' | 'select' | 'radio' | 'checkbox' | 'slider' | 'goods' | 'link' | 'list' | 'custom' | string
  default?: unknown
  required?: boolean
  tips?: string
  options?: Array<{ label: string; value: string | number | boolean }>
  min?: number
  max?: number
}

export type ComponentSchemaGroup = {
  key: string
  title: string
  fields: ComponentSchemaField[]
}

export type ComponentSchema = {
  groups?: ComponentSchemaGroup[]
}

export type ComponentMeta = {
  id: number | string
  component_key: string
  name: string
  category_id?: number | string
  icon?: string
  tpl_id?: number | string
  templates: ComponentTemplate[]
  schema_json?: ComponentSchema
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
