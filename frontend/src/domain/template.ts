export type StoreTemplate = {
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

export type TemplateListParams = {
  page: number
  limit: number
  keyword?: string
  type?: string
  is_sel?: 0 | 1 | ''
}
