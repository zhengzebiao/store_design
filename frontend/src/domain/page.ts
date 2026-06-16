import type { DesignComponent } from './component'

export type StoreDesignPage = {
  id: number | string
  diy_id: number | string
  company_id?: number | string
  type: 'home_page' | 'project_page' | string
  page_name: string
  datas: DesignComponent[]
  other_company_show?: 0 | 1
  page_info: Record<string, unknown>
  member_level?: number[] | string | null
  level: unknown[]
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

export type SavePagePayload = StoreDesignPage & {
  mode: 'create' | 'edit' | 'copy'
  route_id?: string | number
  head_img?: string
}

export type SavePageResult = {
  id: string
  diy_id: string
  url: string
  message: string
}
